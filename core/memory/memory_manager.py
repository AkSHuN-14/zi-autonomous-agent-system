"""
Memory Manager Implementation
Handles dynamic context injection and aggressive summarization
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class MemoryEntry:
    """Single entry in the agent's memory"""
    timestamp: datetime
    entry_type: str  # "observation", "action", "reflection", "constraint"
    content: Any
    importance: float  # 0.0 to 1.0
    tags: List[str] = field(default_factory=list)
    token_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "entry_type": self.entry_type,
            "content": self.content,
            "importance": self.importance,
            "tags": self.tags,
            "token_count": self.token_count
        }


@dataclass
class ContextSummary:
    """Summarized context for injection into agent prompts"""
    recent_actions: List[str] = field(default_factory=list)
    key_observations: List[str] = field(default_factory=list)
    error_reflections: List[str] = field(default_factory=list)
    learned_constraints: List[str] = field(default_factory=list)
    goal_milestones: List[str] = field(default_factory=list)
    total_tokens_used: int = 0
    summary_timestamp: datetime = field(default_factory=datetime.now)
    
    def to_prompt_section(self) -> str:
        """
        Generate the dynamic context section for prompt injection
        
        This follows the blueprint's requirement for aggressive summarization
        to save tokens and maintain context efficiency.
        """
        sections = []
        
        if self.recent_actions:
            sections.append("Recent Actions:")
            for action in self.recent_actions:
                sections.append(f"  - {action}")
        
        if self.key_observations:
            sections.append("Key Observations:")
            for obs in self.key_observations:
                sections.append(f"  - {obs}")
        
        if self.error_reflections:
            sections.append("Error Reflections:")
            for reflection in self.error_reflections:
                sections.append(f"  - {reflection}")
        
        if self.learned_constraints:
            sections.append("Learned Constraints:")
            for constraint in self.learned_constraints:
                sections.append(f"  - {constraint}")
        
        if self.goal_milestones:
            sections.append("Goal Milestones:")
            for milestone in self.goal_milestones:
                sections.append(f"  - {milestone}")
        
        if self.total_tokens_used > 0:
            sections.append(f"Total Tokens Used: {self.total_tokens_used}")
        
        return "\n".join(sections)


class MemoryManager:
    """
    Manages agent memory with aggressive summarization
    
    Implements the memory injection protocol from the blueprint:
    - Dynamic summarization of operational history
    - Context optimization to handle finite context length
    - Priority-based storage of high-impact observations
    """
    
    def __init__(
        self,
        max_memory_entries: int = 1000,
        max_context_tokens: int = 2000,
        importance_threshold: float = 0.3
    ):
        """
        Initialize memory manager
        
        Args:
            max_memory_entries: Maximum number of memory entries to store
            max_context_tokens: Maximum tokens for context injection
            importance_threshold: Minimum importance for long-term storage
        """
        self.max_memory_entries = max_memory_entries
        self.max_context_tokens = max_context_tokens
        self.importance_threshold = importance_threshold
        
        self.memory: List[MemoryEntry] = []
        self.long_term_memory: List[MemoryEntry] = []
        
    def add_entry(
        self,
        entry_type: str,
        content: Any,
        importance: float = 0.5,
        tags: List[str] = None
    ) -> None:
        """
        Add a new entry to memory
        
        Args:
            entry_type: Type of memory entry
            content: Content of the memory
            importance: Importance score (0.0 to 1.0)
            tags: Tags for categorization
        """
        if tags is None:
            tags = []
        
        # Estimate token count
        token_count = self._estimate_tokens(content)
        
        entry = MemoryEntry(
            timestamp=datetime.now(),
            entry_type=entry_type,
            content=content,
            importance=importance,
            tags=tags,
            token_count=token_count
        )
        
        # Add to working memory
        self.memory.append(entry)
        
        # Move important entries to long-term memory
        if importance >= self.importance_threshold:
            self.long_term_memory.append(entry)
        
        # Prune working memory if necessary
        self._prune_memory()
    
    def _estimate_tokens(self, content: Any) -> int:
        """Estimate token count for content"""
        if isinstance(content, str):
            # Rough estimate: ~4 characters per token
            return len(content) // 4
        elif isinstance(content, dict):
            return len(json.dumps(content)) // 4
        else:
            return len(str(content)) // 4
    
    def _prune_memory(self) -> None:
        """Prune memory to stay within limits"""
        # Prune working memory
        if len(self.memory) > self.max_memory_entries:
            # Remove least important entries first
            self.memory.sort(key=lambda x: x.importance)
            remove_count = len(self.memory) - self.max_memory_entries
            self.memory = self.memory[remove_count:]
            # Sort back by timestamp
            self.memory.sort(key=lambda x: x.timestamp)
        
        # Prune long-term memory (more aggressive)
        if len(self.long_term_memory) > self.max_memory_entries // 2:
            self.long_term_memory.sort(key=lambda x: x.importance)
            remove_count = len(self.long_term_memory) - (self.max_memory_entries // 2)
            self.long_term_memory = self.long_term_memory[remove_count:]
            self.long_term_memory.sort(key=lambda x: x.timestamp)
    
    def get_recent_entries(
        self,
        entry_type: Optional[str] = None,
        count: int = 10
    ) -> List[MemoryEntry]:
        """
        Get recent memory entries
        
        Args:
            entry_type: Filter by entry type
            count: Maximum number of entries to return
        """
        filtered = self.memory
        
        if entry_type:
            filtered = [e for e in filtered if e.entry_type == entry_type]
        
        # Return most recent
        return filtered[-count:]
    
    def search_by_tags(self, tags: List[str]) -> List[MemoryEntry]:
        """Search memory entries by tags"""
        results = []
        for entry in self.memory + self.long_term_memory:
            if any(tag in entry.tags for tag in tags):
                results.append(entry)
        return results
    
    def generate_context_summary(self, max_tokens: Optional[int] = None) -> ContextSummary:
        """
        Generate aggressive context summary for injection
        
        This implements the blueprint's requirement for context optimization
        and summarization to handle finite context length constraints.
        """
        if max_tokens is None:
            max_tokens = self.max_context_tokens
        
        summary = ContextSummary()
        current_tokens = 0
        
        # Prioritize recent, high-impact observations
        recent_observations = [
            e for e in self.memory
            if e.entry_type == "observation" and e.importance > 0.6
        ]
        
        for obs in sorted(recent_observations, key=lambda x: x.timestamp, reverse=True)[:5]:
            if current_tokens + obs.token_count <= max_tokens:
                summary.key_observations.append(str(obs.content)[:200])  # Truncate
                current_tokens += obs.token_count
        
        # Add recent actions
        recent_actions = [
            e for e in self.memory
            if e.entry_type == "action"
        ]
        
        for action in sorted(recent_actions, key=lambda x: x.timestamp, reverse=True)[:5]:
            if current_tokens + action.token_count <= max_tokens:
                summary.recent_actions.append(str(action.content)[:150])
                current_tokens += action.token_count
        
        # Add error reflections (high priority)
        error_entries = [
            e for e in self.memory
            if e.entry_type == "reflection" and "error" in e.tags
        ]
        
        for error in sorted(error_entries, key=lambda x: x.timestamp, reverse=True)[:3]:
            if current_tokens + error.token_count <= max_tokens:
                summary.error_reflections.append(str(error.content)[:200])
                current_tokens += error.token_count
        
        # Add learned constraints
        constraint_entries = [
            e for e in self.long_term_memory
            if e.entry_type == "constraint"
        ]
        
        for constraint in constraint_entries[:5]:
            if current_tokens + constraint.token_count <= max_tokens:
                summary.learned_constraints.append(str(constraint.content)[:150])
                current_tokens += constraint.token_count
        
        # Calculate total tokens
        summary.total_tokens_used = sum(e.token_count for e in self.memory)
        
        return summary
    
    def add_constraint(self, constraint: str, importance: float = 0.8) -> None:
        """
        Add a learned constraint to long-term memory
        
        These constraints are injected into future prompt cycles
        to refine agent behavior.
        """
        self.add_entry(
            entry_type="constraint",
            content=constraint,
            importance=importance,
            tags=["constraint", "learned"]
        )
    
    def add_goal_milestone(self, milestone: str, importance: float = 0.9) -> None:
        """Add a goal milestone to memory"""
        self.add_entry(
            entry_type="milestone",
            content=milestone,
            importance=importance,
            tags=["goal", "milestone"]
        )
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get statistics about memory usage"""
        total_tokens = sum(e.token_count for e in self.memory)
        long_term_tokens = sum(e.token_count for e in self.long_term_memory)
        
        return {
            "total_entries": len(self.memory),
            "long_term_entries": len(self.long_term_memory),
            "total_tokens": total_tokens,
            "long_term_tokens": long_term_tokens,
            "average_importance": sum(e.importance for e in self.memory) / len(self.memory) if self.memory else 0,
            "entry_types": self._count_by_type()
        }
    
    def _count_by_type(self) -> Dict[str, int]:
        """Count entries by type"""
        counts = {}
        for entry in self.memory:
            counts[entry.entry_type] = counts.get(entry.entry_type, 0) + 1
        return counts
    
    def export_memory(self, filepath: str) -> None:
        """Export memory to JSON file"""
        export_data = {
            "memory": [entry.to_dict() for entry in self.memory],
            "long_term_memory": [entry.to_dict() for entry in self.long_term_memory],
            "statistics": self.get_memory_statistics()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def import_memory(self, filepath: str) -> None:
        """Import memory from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.memory = []
        for entry_data in data.get("memory", []):
            entry = MemoryEntry(
                timestamp=datetime.fromisoformat(entry_data["timestamp"]),
                entry_type=entry_data["entry_type"],
                content=entry_data["content"],
                importance=entry_data["importance"],
                tags=entry_data.get("tags", []),
                token_count=entry_data.get("token_count", 0)
            )
            self.memory.append(entry)
        
        # Similar for long-term memory
        self.long_term_memory = []
        for entry_data in data.get("long_term_memory", []):
            entry = MemoryEntry(
                timestamp=datetime.fromisoformat(entry_data["timestamp"]),
                entry_type=entry_data["entry_type"],
                content=entry_data["content"],
                importance=entry_data["importance"],
                tags=entry_data.get("tags", []),
                token_count=entry_data.get("token_count", 0)
            )
            self.long_term_memory.append(entry)
