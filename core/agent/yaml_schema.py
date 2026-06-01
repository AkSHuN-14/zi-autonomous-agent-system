"""
YAML Schema Definition for Agent Actions
Defines the mandatory structured output format for all agent actions
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class ActionType(Enum):
    """Enumeration of valid action types"""
    TOOL_USE = "TOOL_USE"
    CLARIFY_REQUEST = "CLARIFY_REQUEST"
    FINAL_ANSWER = "FINAL_ANSWER"


@dataclass
class ToolArguments:
    """Structured tool arguments"""
    arguments: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return self.arguments
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ToolArguments':
        return cls(arguments=data)


@dataclass
class AgentAction:
    """
    Mandatory YAML Schema for Agent Actions
    
    This schema must be strictly followed for all agent outputs to ensure
    reliable parsing and execution by the Agent Execution Environment (AEE).
    
    Schema Fields:
    - Plan_ID: Sequential integer identifier for the current planning cycle
    - Thought: Internal reasoning and justification for the action
    - Action_Type: One of TOOL_USE, CLARIFY_REQUEST, or FINAL_ANSWER
    - Tool_Name: Namespaced tool identifier (conditional on TOOL_USE)
    - Tool_Arguments: Key-value parameters for tool invocation (conditional)
    - Stop_Condition: Boolean flag to halt execution for human review
    """
    
    Plan_ID: int
    Thought: str
    Action_Type: ActionType
    Tool_Name: Optional[str] = None
    Tool_Arguments: Optional[ToolArguments] = None
    Stop_Condition: bool = False
    
    def to_yaml(self) -> str:
        """Convert action to YAML format"""
        yaml_lines = [
            "---",
            f"Plan_ID: {self.Plan_ID}",
            f"Thought: {self.Thought}",
            f"Action_Type: {self.Action_Type.value}"
        ]
        
        if self.Tool_Name:
            yaml_lines.append(f"Tool_Name: {self.Tool_Name}")
        
        if self.Tool_Arguments:
            yaml_lines.append("Tool_Arguments:")
            for key, value in self.Tool_Arguments.to_dict().items():
                yaml_lines.append(f"  {key}: {value}")
        
        yaml_lines.append(f"Stop_Condition: {str(self.Stop_Condition).upper()}")
        yaml_lines.append("---")
        
        return "\n".join(yaml_lines)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert action to dictionary format"""
        result = {
            "Plan_ID": self.Plan_ID,
            "Thought": self.Thought,
            "Action_Type": self.Action_Type.value,
            "Stop_Condition": self.Stop_Condition
        }
        
        if self.Tool_Name:
            result["Tool_Name"] = self.Tool_Name
        
        if self.Tool_Arguments:
            result["Tool_Arguments"] = self.Tool_Arguments.to_dict()
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentAction':
        """Create action from dictionary format"""
        action_type = ActionType(data.get("Action_Type", "TOOL_USE"))
        
        tool_args = None
        if "Tool_Arguments" in data:
            tool_args = ToolArguments.from_dict(data["Tool_Arguments"])
        
        return cls(
            Plan_ID=data.get("Plan_ID", 0),
            Thought=data.get("Thought", ""),
            Action_Type=action_type,
            Tool_Name=data.get("Tool_Name"),
            Tool_Arguments=tool_args,
            Stop_Condition=data.get("Stop_Condition", False)
        )
    
    def validate(self) -> bool:
        """Validate action against schema requirements"""
        # Required fields
        if not isinstance(self.Plan_ID, int) or self.Plan_ID < 0:
            return False
        
        if not isinstance(self.Thought, str) or len(self.Thought) == 0:
            return False
        
        if not isinstance(self.Action_Type, ActionType):
            return False
        
        if not isinstance(self.Stop_Condition, bool):
            return False
        
        # Conditional validation
        if self.Action_Type == ActionType.TOOL_USE:
            if not self.Tool_Name or not isinstance(self.Tool_Name, str):
                return False
            if not self.Tool_Arguments:
                return False
        
        return True


# Schema validation functions
def validate_yaml_action(yaml_string: str) -> bool:
    """Validate YAML string against action schema"""
    try:
        import yaml
        data = yaml.safe_load(yaml_string)
        action = AgentAction.from_dict(data)
        return action.validate()
    except Exception:
        return False


def parse_yaml_action(yaml_string: str) -> AgentAction:
    """Parse YAML string into AgentAction object"""
    import yaml
    data = yaml.safe_load(yaml_string)
    return AgentAction.from_dict(data)
