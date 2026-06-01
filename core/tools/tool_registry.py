"""
Tool Registry and Management
Implements namespaced tool system with strict specifications
"""

from typing import Dict, Callable, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import inspect


class ToolCategory(Enum):
    """Categories of tools for namespacing"""
    WEB_SEARCH = "web_search"
    DATABASE = "database"
    FILE_IO = "file_io"
    API = "api"
    ANALYSIS = "analysis"
    CONTENT = "content"


@dataclass
class ToolParameter:
    """Specification for a tool parameter"""
    name: str
    type: str
    required: bool
    description: str
    default: Any = None


@dataclass
class ToolSpecification:
    """
    Complete specification for a tool
    
    This ensures tools are explicitly defined with clear input/output specifications,
    following the blueprint's requirement for high-quality tool descriptions.
    """
    name: str
    namespace: str
    category: ToolCategory
    description: str
    parameters: List[ToolParameter] = field(default_factory=list)
    return_description: str = ""
    cost_tokens: int = 0
    guardrails: List[str] = field(default_factory=list)
    
    @property
    def full_name(self) -> str:
        """Get the full namespaced tool name"""
        return f"{self.namespace}_{self.name}"
    
    def validate_arguments(self, arguments: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate tool arguments against specification
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required parameters
        for param in self.parameters:
            if param.required and param.name not in arguments:
                return False, f"Required parameter '{param.name}' is missing"
        
        # Check parameter types
        for param in self.parameters:
            if param.name in arguments:
                value = arguments[param.name]
                if not self._validate_type(value, param.type):
                    return False, f"Parameter '{param.name}' has incorrect type. Expected {param.type}"
        
        return True, None
    
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate value against expected type"""
        type_mapping = {
            "string": str,
            "integer": int,
            "float": float,
            "boolean": bool,
            "list": list,
            "dict": dict
        }
        
        expected_python_type = type_mapping.get(expected_type, str)
        return isinstance(value, expected_python_type)


class ToolRegistry:
    """
    Central registry for all available tools
    
    Implements mandatory namespacing and boundary definition to prevent
    functional overlap and agent confusion.
    """
    
    def __init__(self):
        self.tools: Dict[str, ToolSpecification] = {}
        self.implementations: Dict[str, Callable] = {}
    
    def register_tool(
        self,
        specification: ToolSpecification,
        implementation: Callable
    ) -> bool:
        """
        Register a new tool with its specification and implementation
        
        Args:
            specification: Tool specification object
            implementation: Function that implements the tool
            
        Returns:
            True if registration successful, False otherwise
        """
        full_name = specification.full_name
        
        # Check for naming conflicts
        if full_name in self.tools:
            return False
        
        # Validate implementation signature matches specification
        sig = inspect.signature(implementation)
        spec_params = {p.name for p in specification.parameters}
        impl_params = set(sig.parameters.keys())
        
        # Allow for 'self' parameter in methods
        impl_params.discard('self')
        
        if not spec_params.issubset(impl_params):
            return False
        
        self.tools[full_name] = specification
        self.implementations[full_name] = implementation
        
        return True
    
    def get_tool(self, full_name: str) -> Optional[ToolSpecification]:
        """Get tool specification by full name"""
        return self.tools.get(full_name)
    
    def get_tools_by_namespace(self, namespace: str) -> List[ToolSpecification]:
        """Get all tools in a specific namespace"""
        return [
            spec for spec in self.tools.values()
            if spec.namespace == namespace
        ]
    
    def get_tools_by_category(self, category: ToolCategory) -> List[ToolSpecification]:
        """Get all tools in a specific category"""
        return [
            spec for spec in self.tools.values()
            if spec.category == category
        ]
    
    def list_all_tools(self) -> List[str]:
        """List all registered tool names"""
        return list(self.tools.keys())
    
    def execute_tool(self, full_name: str, arguments: Dict[str, Any]) -> tuple[bool, Any, Optional[str]]:
        """
        Execute a tool by name with arguments
        
        Args:
            full_name: Full namespaced tool name
            arguments: Dictionary of tool arguments
            
        Returns:
            Tuple of (success, result, error_message)
        """
        # Get tool specification
        spec = self.get_tool(full_name)
        if not spec:
            return False, None, f"Tool '{full_name}' not found"
        
        # Validate arguments
        is_valid, error_msg = spec.validate_arguments(arguments)
        if not is_valid:
            return False, None, error_msg
        
        # Check guardrails
        for guardrail in spec.guardrails:
            if not self._check_guardrail(guardrail, arguments):
                return False, None, f"Guardrail violation: {guardrail}"
        
        # Execute implementation
        try:
            implementation = self.implementations[full_name]
            result = implementation(**arguments)
            return True, result, None
        except Exception as e:
            return False, None, f"Execution error: {str(e)}"
    
    def _check_guardrail(self, guardrail: str, arguments: Dict[str, Any]) -> bool:
        """Check if a guardrail condition is met"""
        # Simplified guardrail checking
        # In production, this would be more sophisticated
        if "max_results" in guardrail and "max_results" in arguments:
            return arguments["max_results"] <= 5
        return True
    
    def get_tool_description_for_prompt(self, full_name: str) -> str:
        """
        Generate a tool description suitable for inclusion in prompts
        
        This follows the blueprint's requirement for high-quality tool
        descriptions that are explicit about expected inputs and outputs.
        """
        spec = self.get_tool(full_name)
        if not spec:
            return ""
        
        description = f"Tool: {spec.full_name}\n"
        description += f"Description: {spec.description}\n"
        
        if spec.parameters:
            description += "Parameters:\n"
            for param in spec.parameters:
                required = "Required" if param.required else "Optional"
                description += f"  - {param.name} ({param.type}, {required}): {param.description}\n"
        
        if spec.return_description:
            description += f"Returns: {spec.return_description}\n"
        
        if spec.cost_tokens > 0:
            description += f"Token Cost: {spec.cost_tokens}\n"
        
        if spec.guardrails:
            description += "Guardrails:\n"
            for guardrail in spec.guardrails:
                description += f"  - {guardrail}\n"
        
        return description
    
    def generate_all_tools_prompt(self) -> str:
        """Generate a complete prompt section with all tool descriptions"""
        tools_section = "### AVAILABLE TOOLS AND SPECIFICATIONS ###\n\n"
        
        for tool_name in self.list_all_tools():
            tools_section += self.get_tool_description_for_prompt(tool_name) + "\n"
        
        return tools_section


# Global tool registry instance
global_registry = ToolRegistry()


# Convenience functions for tool registration
def register_tool(
    name: str,
    namespace: str,
    category: ToolCategory,
    description: str,
    parameters: List[ToolParameter],
    return_description: str = "",
    cost_tokens: int = 0,
    guardrails: List[str] = None
):
    """
    Decorator for registering tools
    
    Usage:
        @register_tool(
            name="search",
            namespace="web",
            category=ToolCategory.WEB_SEARCH,
            description="Search the web for information",
            parameters=[
                ToolParameter("query", "string", True, "Search query"),
                ToolParameter("max_results", "integer", False, "Maximum results", 5)
            ]
        )
        def web_search(query: str, max_results: int = 5):
            # Implementation
            pass
    """
    def decorator(implementation):
        spec = ToolSpecification(
            name=name,
            namespace=namespace,
            category=category,
            description=description,
            parameters=parameters,
            return_description=return_description,
            cost_tokens=cost_tokens,
            guardrails=guardrails or []
        )
        global_registry.register_tool(spec, implementation)
        return implementation
    
    return decorator
