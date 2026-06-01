# ZI Agent System Setup Guide

## Quick Start

### 1. Installation

```bash
# Navigate to agent-system directory
cd agent-system

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

```python
from core.agent.main import create_agent

# Create and initialize agent
agent = create_agent(user_id="TA'K$HUN")

# Execute a task
results = agent.execute_task("Search for information about autonomous agents")

# Check results
print(f"Success: {results['success']}")
print(f"Final Answer: {results['final_answer']}")

# Check agent status
status = agent.get_agent_status()
print(f"Memory Stats: {status['memory_stats']}")
```

### 3. Web Interface

Open the Agent Execution Environment (AEE) web interface:

```bash
# Simply open the HTML file in your browser
open execution/web/index.html
```

Or serve it with a local web server:

```bash
# Using Python
cd execution/web
python -m http.server 8000

# Then navigate to http://localhost:8000
```

## Architecture Overview

### Core Components

1. **Agent Architecture** (`core/agent/`)
   - `yaml_schema.py`: Defines the mandatory YAML schema for agent actions
   - `react_loop.py`: Implements the ReAct (Reason + Act) execution loop
   - `main.py`: Main agent integration class

2. **Tool Management** (`core/tools/`)
   - `tool_registry.py`: Central registry with namespacing and validation
   - `example_tools.py`: Example tool implementations (web search, database, file I/O, etc.)

3. **Memory System** (`core/memory/`)
   - `memory_manager.py`: Context injection and aggressive summarization

4. **Security Layer** (`core/guardrails/`)
   - `security_layer.py`: Multi-layer guardrails with personalized criteria for TA'K$HUN

5. **Execution Environment** (`execution/web/`)
   - `index.html`: Web-based AEE interface for agent interaction

### Key Features

- **ReAct Loop**: Thought → Action → Observation → Reflection cycle
- **Structured Output**: Mandatory YAML schema for all actions
- **Self-Correction**: LATS-style reflection and inverse prompting
- **Cost Optimization**: Token-efficient operations and context management
- **Security**: Multi-layer guardrails with PII protection
- **Personalized Criteria**: Special handling for TA'K$HUN as per blueprint

## Configuration

Edit `config/settings.yaml` to customize:

- Agent behavior (max iterations, error threshold)
- Memory settings (max entries, context tokens)
- Security preferences
- Tool configurations
- Personalized criteria for trusted users

## Examples

### Custom Tool Registration

```python
from core.tools.tool_registry import register_tool, ToolParameter, ToolCategory

@register_tool(
    name="my_tool",
    namespace="custom",
    category=ToolCategory.API,
    description="My custom tool",
    parameters=[
        ToolParameter("input", "string", True, "Input parameter")
    ]
)
def my_custom_tool(input: str) -> str:
    return f"Processed: {input}"
```

### Memory Management

```python
# Add custom memory entry
agent.memory_manager.add_entry(
    entry_type="custom",
    content="Important information",
    importance=0.9,
    tags=["important"]
)

# Add learned constraint
agent.memory_manager.add_constraint(
    "Avoid actions that cause timeout errors",
    importance=0.8
)

# Get context summary
summary = agent.memory_manager.generate_context_summary()
print(summary.to_prompt_section())
```

### Security Checks

```python
# Manual security check
content = "Some user input"
is_safe, violations = agent.security_layer.check_system_integrity(content, user_id)

if not is_safe:
    print(f"Security violations: {[v.description for v in violations]}")
```

## Advanced Usage

### Tree of Thought (ToT) Mode

For complex tasks, the agent can simulate Tree of Thought reasoning:

```python
# The agent will automatically trigger ToT for complex tasks
results = agent.execute_task("Optimize platform SEO, interaction, participation and retention for maximum monetization")
```

### Inverse Prompting for Plan Validation

The agent automatically performs inverse prompting for multi-step plans:

```python
# Agent will validate plan coherence before execution
results = agent.execute_task("Create a multi-step plan for system migration")
```

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`

2. **Tool not found**: Ensure tools are registered before use. Check with `agent.get_agent_status()['available_tools']`

3. **Memory overflow**: Adjust `max_memory_entries` in settings.yaml

4. **Security violations**: Check violation log in `data/violations.json`

### Debug Mode

Enable debug mode in `config/settings.yaml`:

```yaml
development:
  debug_mode: true
  verbose_logging: true
```

## Next Steps

1. Customize tools for your specific use case
2. Adjust security criteria for your requirements
3. Integrate with actual LLM API for thought generation
4. Deploy to production environment
5. Add custom UI/UX as needed

## Support

For issues or questions about the ZI Agent System, refer to the main blueprint document `ZI.io_imp_1_2.md` for architectural details.
