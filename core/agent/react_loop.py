"""
ReAct (Reason + Act) Loop Implementation
Core execution engine for the autonomous agent
"""

from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass
from enum import Enum
import time

from .yaml_schema import AgentAction, ActionType


class LoopState(Enum):
    """States in the ReAct loop"""
    THOUGHT = "THOUGHT"
    ACTION = "ACTION"
    OBSERVATION = "OBSERVATION"
    REFLECTION = "REFLECTION"
    COMPLETED = "COMPLETED"
    HALTED = "HALTED"


@dataclass
class LoopContext:
    """Context maintained throughout the ReAct loop"""
    plan_id: int = 0
    history: list = None
    learned_constraints: list = None
    error_reflections: list = None
    token_count: int = 0
    
    def __post_init__(self):
        if self.history is None:
            self.history = []
        if self.learned_constraints is None:
            self.learned_constraints = []
        if self.error_reflections is None:
            self.error_reflections = []


@dataclass
class Observation:
    """Result from tool execution or external environment"""
    success: bool
    data: Any
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ReActLoop:
    """
    ReAct (Reason + Act) Loop Implementation
    
    This class implements the cyclical execution mechanism:
    Thought → Action → Observation → Reflection
    
    The loop continues until:
    - Final answer is reached
    - Stop condition is triggered
    - Maximum iterations are reached
    - Error threshold is exceeded
    """
    
    def __init__(
        self,
        thought_generator: Callable[[LoopContext], str],
        tool_executor: Callable[[str, Dict[str, Any]], Observation],
        reflection_generator: Optional[Callable[[Observation, LoopContext], str]] = None,
        max_iterations: int = 50,
        error_threshold: int = 3
    ):
        """
        Initialize ReAct loop
        
        Args:
            thought_generator: Function to generate thoughts from context
            tool_executor: Function to execute tool calls
            reflection_generator: Optional function for self-reflection
            max_iterations: Maximum number of loop iterations
            error_threshold: Maximum consecutive errors before halting
        """
        self.thought_generator = thought_generator
        self.tool_executor = tool_executor
        self.reflection_generator = reflection_generator
        self.max_iterations = max_iterations
        self.error_threshold = error_threshold
        
        self.context = LoopContext()
        self.state = LoopState.THOUGHT
        self.consecutive_errors = 0
    
    def generate_thought(self) -> str:
        """Generate the next thought based on current context"""
        self.state = LoopState.THOUGHT
        thought = self.thought_generator(self.context)
        
        # Track token usage (simplified estimation)
        self.context.token_count += len(thought.split())
        
        return thought
    
    def parse_action_from_thought(self, thought: str) -> AgentAction:
        """
        Parse structured action from thought
        In a real implementation, this would use LLM to extract YAML
        """
        # This is a simplified version - real implementation would use
        # an LLM to generate the structured YAML action from the thought
        # For now, we return a placeholder
        return AgentAction(
            Plan_ID=self.context.plan_id,
            Thought=thought,
            Action_Type=ActionType.TOOL_USE,
            Tool_Name="placeholder_tool",
            Tool_Arguments=None,
            Stop_Condition=False
        )
    
    def execute_action(self, action: AgentAction) -> Observation:
        """Execute the parsed action"""
        self.state = LoopState.ACTION
        
        # Check stop condition
        if action.Stop_Condition:
            self.state = LoopState.HALTED
            return Observation(
                success=True,
                data="Execution halted by stop condition - awaiting human review",
                metadata={"halted_by_stop_condition": True}
            )
        
        # Handle different action types
        if action.Action_Type == ActionType.FINAL_ANSWER:
            self.state = LoopState.COMPLETED
            return Observation(
                success=True,
                data=action.Thought,
                metadata={"final_answer": True}
            )
        
        elif action.Action_Type == ActionType.CLARIFY_REQUEST:
            self.state = LoopState.HALTED
            return Observation(
                success=True,
                data=f"Clarification requested: {action.Thought}",
                metadata={"clarification_needed": True}
            )
        
        elif action.Action_Type == ActionType.TOOL_USE:
            if not action.Tool_Name or not action.Tool_Arguments:
                error = "Tool use requires Tool_Name and Tool_Arguments"
                self.consecutive_errors += 1
                return Observation(
                    success=False,
                    data=None,
                    error_message=error
                )
            
            # Execute the tool
            observation = self.tool_executor(
                action.Tool_Name,
                action.Tool_Arguments.to_dict()
            )
            
            if observation.success:
                self.consecutive_errors = 0
            else:
                self.consecutive_errors += 1
            
            return observation
        
        else:
            error = f"Unknown action type: {action.Action_Type}"
            self.consecutive_errors += 1
            return Observation(
                success=False,
                data=None,
                error_message=error
            )
    
    def reflect(self, observation: Observation, action: AgentAction) -> str:
        """Generate reflection on the observation"""
        self.state = LoopState.REFLECTION
        
        if not self.reflection_generator:
            return "No reflection generator configured"
        
        reflection = self.reflection_generator(observation, self.context)
        
        # Store error reflections for future reference
        if not observation.success and observation.error_message:
            self.context.error_reflections.append({
                "plan_id": self.context.plan_id,
                "error": observation.error_message,
                "reflection": reflection,
                "action": action.to_dict()
            })
        
        return reflection
    
    def update_context(self, thought: str, action: AgentAction, observation: Observation):
        """Update the loop context with the latest cycle"""
        self.context.history.append({
            "plan_id": self.context.plan_id,
            "thought": thought,
            "action": action.to_dict(),
            "observation": {
                "success": observation.success,
                "data": observation.data,
                "error": observation.error_message
            }
        })
        
        # Increment plan ID for next cycle
        self.context.plan_id += 1
    
    def should_continue(self) -> bool:
        """Determine if the loop should continue"""
        # Check if we've reached final state
        if self.state in [LoopState.COMPLETED, LoopState.HALTED]:
            return False
        
        # Check max iterations
        if self.context.plan_id >= self.max_iterations:
            return False
        
        # Check error threshold
        if self.consecutive_errors >= self.error_threshold:
            return False
        
        return True
    
    def run(self, initial_thought: str = "") -> Dict[str, Any]:
        """
        Run the complete ReAct loop
        
        Args:
            initial_thought: Optional starting thought for the loop
            
        Returns:
            Dictionary containing loop results and statistics
        """
        results = {
            "completed": False,
            "halted": False,
            "iterations": 0,
            "final_answer": None,
            "total_tokens": 0,
            "errors": []
        }
        
        # Set initial thought if provided
        if initial_thought:
            thought = initial_thought
        else:
            thought = self.generate_thought()
        
        while self.should_continue():
            try:
                # Parse action from thought
                action = self.parse_action_from_thought(thought)
                
                # Execute action
                observation = self.execute_action(action)
                
                # Reflect on results
                reflection = self.reflect(observation, action)
                
                # Update context
                self.update_context(thought, action, observation)
                
                # Generate next thought
                if self.state not in [LoopState.COMPLETED, LoopState.HALTED]:
                    thought = self.generate_thought()
                
                results["iterations"] += 1
                
            except Exception as e:
                self.consecutive_errors += 1
                results["errors"].append(str(e))
                
                if self.consecutive_errors >= self.error_threshold:
                    break
        
        # Compile final results
        results["completed"] = (self.state == LoopState.COMPLETED)
        results["halted"] = (self.state == LoopState.HALTED)
        results["final_answer"] = self.context.history[-1]["observation"]["data"] if self.context.history else None
        results["total_tokens"] = self.context.token_count
        
        return results


# Example implementations
def example_thought_generator(context: LoopContext) -> str:
    """Example thought generator"""
    if context.plan_id == 0:
        return "I need to understand the user's request and determine the best approach."
    else:
        return f"Continuing with plan ID {context.plan_id}, analyzing previous results."


def example_tool_executor(tool_name: str, arguments: Dict[str, Any]) -> Observation:
    """Example tool executor"""
    return Observation(
        success=True,
        data=f"Executed {tool_name} with arguments {arguments}",
        metadata={"tool": tool_name}
    )


def example_reflection_generator(observation: Observation, context: LoopContext) -> str:
    """Example reflection generator"""
    if observation.success:
        return "Action completed successfully, proceeding to next step."
    else:
        return f"Action failed: {observation.error_message}. Need to adjust approach."
