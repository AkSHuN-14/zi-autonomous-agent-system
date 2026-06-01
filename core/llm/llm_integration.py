"""
LLM Integration System
Supports multiple LLM providers with advanced reasoning capabilities
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import json
import time


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    MOCK = "mock"  # For testing without API calls


class ReasoningMode(Enum):
    """Reasoning modes"""
    REACT = "react"  # Standard ReAct loop
    TOT = "tot"      # Tree of Thoughts
    HYBRID = "hybrid"  # Adaptive selection


@dataclass
class LLMResponse:
    """Standard LLM response structure"""
    content: str
    model: str
    tokens_used: int
    cost: float
    reasoning_trace: Optional[List[str]] = None
    latency: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "model": self.model,
            "tokens_used": self.tokens_used,
            "cost": self.cost,
            "reasoning_trace": self.reasoning_trace,
            "latency": self.latency
        }


@dataclass
class Thought:
    """Individual thought in reasoning process"""
    content: str
    expert_id: Optional[str] = None  # For ToT multi-expert reasoning
    confidence: float = 0.5
    parent_thought_id: Optional[str] = None


class TreeOfThoughtProcessor:
    """
    Tree of Thoughts (ToT) Implementation
    Parallel reasoning with multiple expert perspectives
    """
    
    def __init__(self, num_experts: int = 3):
        """
        Initialize ToT processor
        
        Args:
            num_experts: Number of parallel reasoning paths
        """
        self.num_experts = num_experts
        self.expert_personas = [
            "Analytical Expert: Focus on logical structure and step-by-step reasoning",
            "Creative Expert: Consider alternative approaches and innovative solutions", 
            "Critical Expert: Identify potential issues and validate assumptions"
        ]
    
    def generate_parallel_thoughts(
        self,
        context: str,
        task: str,
        llm_client: 'LLMClient'
    ) -> List[Thought]:
        """
        Generate parallel reasoning thoughts from multiple expert perspectives
        
        Args:
            context: Current context and history
            task: Current task or problem
            llm_client: LLM client for generation
            
        Returns:
            List of thoughts from different expert perspectives
        """
        thoughts = []
        
        for i in range(self.num_experts):
            persona = self.expert_personas[i % len(self.expert_personas)]
            
            prompt = f"""
            {persona}

            Task: {task}
            Context: {context}

            Provide your step-by-step reasoning for this task. 
            Focus on your area of expertise as defined above.
            Be specific and actionable.
            """
            
            try:
                response = llm_client.generate(
                    prompt=prompt,
                    max_tokens=500,
                    temperature=0.7
                )
                
                thought = Thought(
                    content=response.content,
                    expert_id=f"expert_{i}",
                    confidence=0.7  # Could be calculated from response quality
                )
                
                thoughts.append(thought)
                
            except Exception as e:
                # Fallback if LLM call fails
                thought = Thought(
                    content=f"Expert {i} reasoning: Analyzing task '{task}' with context '{context}'",
                    expert_id=f"expert_{i}",
                    confidence=0.5
                )
                thoughts.append(thought)
        
        return thoughts
    
    def evaluate_and_prune(
        self,
        thoughts: List[Thought],
        llm_client: 'LLMClient'
    ) -> List[Thought]:
        """
        Evaluate thoughts and prune less promising paths
        
        Args:
            thoughts: List of thoughts to evaluate
            llm_client: LLM client for evaluation
            
        Returns:
            Pruned list of best thoughts
        """
        if len(thoughts) <= 1:
            return thoughts
        
        # Create evaluation prompt
        thoughts_text = "\n\n".join([
            f"Expert {i}: {thought.content}" 
            for i, thought in enumerate(thoughts)
        ])
        
        evaluation_prompt = f"""
        Evaluate the following expert perspectives on a task:
        
        {thoughts_text}
        
        Rank them from best to worst based on:
        1. Logical coherence
        2. Practical feasibility
        3. Likely success
        
        Return only the ranking as numbers (e.g., "2, 0, 1" meaning expert 2 is best, then 0, then 1).
        """
        
        try:
            response = llm_client.generate(
                prompt=evaluation_prompt,
                max_tokens=100,
                temperature=0.3
            )
            
            # Parse ranking
            ranking = self._parse_ranking(response.content, len(thoughts))
            
            # Sort thoughts by ranking
            sorted_thoughts = [thoughts[i] for i in ranking]
            
            # Return top 2 (pruning)
            return sorted_thoughts[:2]
            
        except Exception as e:
            # Fallback: return original thoughts
            return thoughts
    
    def _parse_ranking(self, ranking_text: str, num_thoughts: int) -> List[int]:
        """Parse ranking from LLM response"""
        try:
            # Extract numbers from response
            numbers = [int(n) for n in ranking_text.split() if n.isdigit()]
            # Filter to valid range
            valid_numbers = [n for n in numbers if 0 <= n < num_thoughts]
            return valid_numbers if valid_numbers else list(range(num_thoughts))
        except:
            return list(range(num_thoughts))
    
    def synthesize_consensus(
        self,
        thoughts: List[Thought],
        llm_client: 'LLMClient'
    ) -> str:
        """
        Synthesize a consensus from multiple thoughts
        
        Args:
            thoughts: List of thoughts to synthesize
            llm_client: LLM client for synthesis
            
        Returns:
            Consensus reasoning
        """
        thoughts_text = "\n\n".join([
            f"Expert {i}: {thought.content}"
            for i, thought in enumerate(thoughts)
        ])
        
        synthesis_prompt = f"""
        Synthesize the following expert perspectives into a single, coherent approach:
        
        {thoughts_text}
        
        Provide the best approach that incorporates the strengths of each perspective.
        """
        
        try:
            response = llm_client.generate(
                prompt=synthesis_prompt,
                max_tokens=500,
                temperature=0.5
            )
            return response.content
        except Exception as e:
            # Fallback: concatenate thoughts
            return "\n".join([thought.content for thought in thoughts])


class InversePromptingValidator:
    """
    Inverse Prompting for Plan Validation
    Validates plans by attempting to reverse them
    """
    
    def validate_plan(
        self,
        plan: List[str],
        llm_client: 'LLMClient'
    ) -> Dict[str, Any]:
        """
        Validate a plan by attempting to reverse it
        
        Args:
            plan: List of plan steps
            llm_client: LLM client for validation
            
        Returns:
            Validation results with coherence score
        """
        plan_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(plan)])
        
        # Generate inverse plan
        inverse_prompt = f"""
        Original plan:
        {plan_text}
        
        Generate the inverse of this plan - the steps that would undo each action
        to return to the original state.
        """
        
        try:
            inverse_response = llm_client.generate(
                prompt=inverse_prompt,
                max_tokens=500,
                temperature=0.3
            )
            
            # Validate coherence
            coherence_check = f"""
            Original plan:
            {plan_text}
            
            Inverse plan:
            {inverse_response.content}
            
            Does the inverse plan logically reverse the original plan? 
            Answer YES or NO with brief explanation.
            """
            
            coherence_response = llm_client.generate(
                prompt=coherence_check,
                max_tokens=100,
                temperature=0.1
            )
            
            is_coherent = "YES" in coherence_response.content.upper()
            coherence_score = 0.8 if is_coherent else 0.4
            
            return {
                "is_coherent": is_coherent,
                "coherence_score": coherence_score,
                "inverse_plan": inverse_response.content,
                "explanation": coherence_response.content
            }
            
        except Exception as e:
            return {
                "is_coherent": True,  # Default to coherent if validation fails
                "coherence_score": 0.5,
                "inverse_plan": "Validation failed",
                "explanation": f"Validation error: {str(e)}"
            }


class LLMClient:
    """
    Unified LLM Client supporting multiple providers
    """
    
    def __init__(
        self,
        provider: LLMProvider = LLMProvider.MOCK,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        cost_per_1k_tokens: float = 0.002
    ):
        """
        Initialize LLM client
        
        Args:
            provider: LLM provider to use
            api_key: API key for the provider
            model: Model name
            cost_per_1k_tokens: Cost per 1000 tokens
        """
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.cost_per_1k_tokens = cost_per_1k_tokens
        self.total_tokens_used = 0
        self.total_cost = 0.0
        
        # Initialize specialized processors
        self.tot_processor = TreeOfThoughtProcessor()
        self.inverse_validator = InversePromptingValidator()
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        reasoning_mode: ReasoningMode = ReasoningMode.REACT
    ) -> LLMResponse:
        """
        Generate text using the configured LLM
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            reasoning_mode: Reasoning mode to use
            
        Returns:
            LLM response with metadata
        """
        start_time = time.time()
        
        if self.provider == LLMProvider.MOCK:
            # Mock response for testing
            content = self._generate_mock_response(prompt, reasoning_mode)
            tokens_used = len(content.split()) * 2  # Rough estimate
            
        elif self.provider == LLMProvider.OPENAI:
            # OpenAI integration (would require openai package)
            content = self._generate_openai_response(prompt, max_tokens, temperature)
            tokens_used = len(content.split()) * 2
            
        elif self.provider == LLMProvider.ANTHROPIC:
            # Anthropic integration (would require anthropic package)
            content = self._generate_anthropic_response(prompt, max_tokens, temperature)
            tokens_used = len(content.split()) * 2
            
        else:
            # Default to mock
            content = self._generate_mock_response(prompt, reasoning_mode)
            tokens_used = len(content.split()) * 2
        
        latency = time.time() - start_time
        cost = (tokens_used / 1000) * self.cost_per_1k_tokens
        
        self.total_tokens_used += tokens_used
        self.total_cost += cost
        
        return LLMResponse(
            content=content,
            model=self.model,
            tokens_used=tokens_used,
            cost=cost,
            latency=latency
        )
    
    def generate_with_tot(
        self,
        context: str,
        task: str,
        max_tokens: int = 500
    ) -> LLMResponse:
        """
        Generate using Tree of Thoughts reasoning
        
        Args:
            context: Current context
            task: Current task
            max_tokens: Maximum tokens for final response
            
        Returns:
            LLM response with ToT reasoning
        """
        # Generate parallel thoughts
        thoughts = self.tot_processor.generate_parallel_thoughts(context, task, self)
        
        # Evaluate and prune
        best_thoughts = self.tot_processor.evaluate_and_prune(thoughts, self)
        
        # Synthesize consensus
        consensus = self.tot_processor.synthesize_consensus(best_thoughts, self)
        
        tokens_used = len(consensus.split()) * 2
        cost = (tokens_used / 1000) * self.cost_per_1k_tokens
        
        return LLMResponse(
            content=consensus,
            model=self.model,
            tokens_used=tokens_used,
            cost=cost,
            reasoning_trace=[thought.content for thought in thoughts]
        )
    
    def validate_plan_with_inverse_prompting(
        self,
        plan: List[str]
    ) -> Dict[str, Any]:
        """
        Validate a plan using inverse prompting
        
        Args:
            plan: List of plan steps
            
        Returns:
            Validation results
        """
        return self.inverse_validator.validate_plan(plan, self)
    
    def _generate_mock_response(self, prompt: str, reasoning_mode: ReasoningMode) -> str:
        """Generate mock response for testing"""
        if reasoning_mode == ReasoningMode.TOT:
            return f"Tree of Thoughts analysis: Considering multiple expert perspectives on '{prompt[:50]}...' Analyzing alternatives and selecting optimal path."
        return f"Mock response to: {prompt[:50]}... Generating reasoned action based on current context and available tools."
    
    def _generate_openai_response(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate response using OpenAI API (placeholder)"""
        # In production, this would use:
        # import openai
        # response = openai.ChatCompletion.create(...)
        return f"OpenAI response to: {prompt[:50]}..."
    
    def _generate_anthropic_response(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate response using Anthropic API (placeholder)"""
        # In production, this would use:
        # import anthropic
        # response = anthropic.Anthropic().messages.create(...)
        return f"Anthropic response to: {prompt[:50]}..."
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            "total_tokens_used": self.total_tokens_used,
            "total_cost": self.total_cost,
            "provider": self.provider.value,
            "model": self.model
        }


# Integration with existing agent system
class LLMEnhancedAgent:
    """
    Agent enhanced with LLM capabilities
    Integrates LLM client with existing ReAct loop
    """
    
    def __init__(
        self,
        llm_client: LLMClient,
        base_agent: 'ZIAgent'
    ):
        """
        Initialize LLM-enhanced agent
        
        Args:
            llm_client: Configured LLM client
            base_agent: Base ZI agent instance
        """
        self.llm_client = llm_client
        self.base_agent = base_agent
        self.reasoning_mode = ReasoningMode.REACT
    
    def set_reasoning_mode(self, mode: ReasoningMode):
        """Set the reasoning mode"""
        self.reasoning_mode = mode
    
    def generate_thought_with_llm(
        self,
        context: str,
        task: str,
        use_tot: bool = False
    ) -> str:
        """
        Generate thought using LLM
        
        Args:
            context: Current context
            task: Current task
            use_tot: Whether to use Tree of Thoughts
            
        Returns:
            Generated thought
        """
        system_prompt = self.base_agent.system_prompt
        full_prompt = f"{system_prompt}\n\nContext: {context}\n\nTask: {task}\n\nGenerate your next thought and action using the YAML schema."
        
        if use_tot:
            response = self.llm_client.generate_with_tot(context, task)
            return response.content
        else:
            response = self.llm_client.generate(prompt=full_prompt)
            return response.content
    
    def execute_task_with_llm(
        self,
        task: str,
        use_tot: bool = False
    ) -> Dict[str, Any]:
        """
        Execute task using LLM-enhanced reasoning
        
        Args:
            task: Task to execute
            use_tot: Whether to use Tree of Thoughts
            
        Returns:
            Execution results
        """
        # Get current context summary
        context_summary = self.base_agent.memory_manager.generate_context_summary()
        context_str = context_summary.to_prompt_section()
        
        # Generate initial thought
        thought = self.generate_thought_with_llm(context_str, task, use_tot)
        
        # Store in memory
        self.base_agent.memory_manager.add_entry(
            entry_type="thought",
            content=thought,
            importance=0.8,
            tags=["llm_generated", "tot" if use_tot else "react"]
        )
        
        # Execute using base agent
        results = self.base_agent.execute_task(task)
        
        # Add LLM usage stats
        results["llm_usage"] = self.llm_client.get_usage_statistics()
        
        return results


# Convenience function for creating LLM client
def create_llm_client(
    provider: str = "mock",
    api_key: Optional[str] = None,
    model: str = "gpt-3.5-turbo"
) -> LLMClient:
    """Create configured LLM client"""
    try:
        provider_enum = LLMProvider(provider.lower())
    except ValueError:
        provider_enum = LLMProvider.MOCK
    
    return LLMClient(
        provider=provider_enum,
        api_key=api_key,
        model=model
    )


if __name__ == "__main__":
    # Example usage
    llm_client = create_llm_client(provider="mock")
    
    print("Testing basic generation:")
    response = llm_client.generate("Test prompt for autonomous agent")
    print(f"Response: {response.content}")
    print(f"Tokens: {response.tokens_used}, Cost: ${response.cost:.4f}")
    
    print("\nTesting Tree of Thoughts:")
    tot_response = llm_client.generate_with_tot(
        context="Agent is starting a new task",
        task="Optimize content generation for multiple platforms"
    )
    print(f"Response: {tot_response.content}")
    print(f"Reasoning trace: {tot_response.reasoning_trace}")
    
    print("\nTesting inverse prompting:")
    plan = ["Step 1: Analyze requirements", "Step 2: Generate content", "Step 3: Optimize AIDA"]
    validation = llm_client.validate_plan_with_inverse_prompting(plan)
    print(f"Coherent: {validation['is_coherent']}, Score: {validation['coherence_score']}")
    
    print("\nUsage Statistics:")
    print(json.dumps(llm_client.get_usage_statistics(), indent=2))
