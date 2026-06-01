"""
Example Tool Implementations
Demonstrates the tool system with namespaced implementations
"""

from typing import Dict, Any, List
from .tool_registry import register_tool, ToolParameter, ToolCategory


@register_tool(
    name="search_engine",
    namespace="web",
    category=ToolCategory.WEB_SEARCH,
    description="Performs an external web search. MANDATE: Set max_results to 5 or fewer to maximize token efficiency.",
    parameters=[
        ToolParameter("query", "string", True, "Search query string"),
        ToolParameter("max_results", "integer", False, "Maximum number of results to return", 5)
    ],
    return_description="List of search results with titles, URLs, and snippets",
    cost_tokens=50,
    guardrails=["max_results must be 5 or fewer"]
)
def web_search_engine(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Example web search implementation
    
    In production, this would call actual search APIs (Google, Bing, etc.)
    """
    # Validate guardrail
    if max_results > 5:
        raise ValueError("max_results cannot exceed 5 per guardrail")
    
    # Simulated results for demonstration
    mock_results = [
        {
            "title": f"Result for: {query}",
            "url": "https://example.com/result1",
            "snippet": f"This is a mock search result for the query '{query}'"
        }
    ]
    
    return mock_results[:max_results]


@register_tool(
    name="query_sql",
    namespace="database",
    category=ToolCategory.DATABASE,
    description="Executes a read-only SQL command against the secure data warehouse",
    parameters=[
        ToolParameter("sql_command", "string", True, "SQL command to execute")
    ],
    return_description="Query results as structured data",
    cost_tokens=30,
    guardrails=["SQL must be read-only (no INSERT, UPDATE, DELETE)"]
)
def db_query_sql(sql_command: str) -> Dict[str, Any]:
    """
    Example database query implementation
    
    In production, this would connect to actual databases
    """
    # Security check for read-only operations
    forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER"]
    sql_upper = sql_command.upper()
    
    for keyword in forbidden_keywords:
        if keyword in sql_upper:
            raise ValueError(f"CRITICAL GUARDRAIL VIOLATION: {keyword} not allowed in read-only SQL")
    
    # Simulated query result
    return {
        "count": 1,
        "data": [{"id": 101, "status": "Active", "region": "NA"}],
        "execution_time": "0.05s"
    }


@register_tool(
    name="write_file",
    namespace="file",
    category=ToolCategory.FILE_IO,
    description="Writes text content to a file. CRITICAL GUARDRAIL: Requires human confirmation for sensitive paths.",
    parameters=[
        ToolParameter("path", "string", True, "File path to write to"),
        ToolParameter("content", "string", True, "Content to write to file")
    ],
    return_description="Confirmation of file write operation",
    cost_tokens=20,
    guardrails=["Requires human confirmation for sensitive paths"]
)
def file_io_write(path: str, content: str) -> str:
    """
    Example file write implementation
    
    In production, this would require human confirmation for sensitive paths
    """
    # Check for sensitive paths
    sensitive_paths = ["/etc", "/system", "/var", "~/.ssh"]
    
    for sensitive in sensitive_paths:
        if path.startswith(sensitive):
            raise PermissionError(
                f"CRITICAL GUARDRAIL: Path '{path}' is sensitive. "
                "Requires Stop_Condition: TRUE and human confirmation."
            )
    
    # In production, actual file write would happen here
    # For demonstration, just return success message
    return f"Successfully wrote content to {path}"


@register_tool(
    name="analyze_sentiment",
    namespace="analysis",
    category=ToolCategory.ANALYSIS,
    description="Analyzes the sentiment of text content",
    parameters=[
        ToolParameter("text", "string", True, "Text to analyze"),
        ToolParameter("detailed", "boolean", False, "Return detailed analysis", False)
    ],
    return_description="Sentiment analysis results with scores and labels",
    cost_tokens=15
)
def analysis_sentiment(text: str, detailed: bool = False) -> Dict[str, Any]:
    """
    Example sentiment analysis implementation
    
    In production, this would use NLP models or APIs
    """
    # Simplified sentiment analysis
    positive_words = ["good", "great", "excellent", "amazing", "wonderful"]
    negative_words = ["bad", "terrible", "awful", "horrible", "poor"]
    
    words = text.lower().split()
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    
    if positive_count > negative_count:
        sentiment = "positive"
        score = 0.7
    elif negative_count > positive_count:
        sentiment = "negative"
        score = 0.3
    else:
        sentiment = "neutral"
        score = 0.5
    
    result = {
        "sentiment": sentiment,
        "score": score,
        "confidence": abs(score - 0.5) * 2
    }
    
    if detailed:
        result["positive_words_found"] = positive_count
        result["negative_words_found"] = negative_count
        result["word_count"] = len(words)
    
    return result


@register_tool(
    name="generate_content",
    namespace="content",
    category=ToolCategory.CONTENT,
    description="Generates content for various platforms with specified tone",
    parameters=[
        ToolParameter("platform", "string", True, "Target platform (FetLife, Chaturbate, Fansly, etc.)"),
        ToolParameter("tone", "string", True, "Content tone (suggestive, explicit, professional)"),
        ToolParameter("topic", "string", False, "Specific topic or theme", "general")
    ],
    return_description="Generated content tailored to the specified platform and tone",
    cost_tokens=100
)
def content_generator(platform: str, tone: str, topic: str = "general") -> str:
    """
    Example content generation implementation
    
    This relates to the FVCGen system mentioned in the blueprint
    """
    # Platform-specific templates
    templates = {
        "FetLife": {
            "explicit": [
                "Dominate your desires and finances with kinky mastery.",
                "Surrender to the contract, let it bind your body and bank."
            ],
            "suggestive": [
                "Unlock your inner potential with a sultry twist on freedom.",
                "Tease your limits with secrets of power and control."
            ]
        },
        "Chaturbate": {
            "explicit": [
                "Watch me perfect your filing, my body writhing as I collateralize your pleasure.",
                "Secured transaction domination: my grip on your collateral is tight."
            ],
            "suggestive": [
                "Join me for an interactive session of financial exploration.",
                "Experience the thrill of controlled transactions live."
            ]
        },
        "Fansly": {
            "explicit": [
                "UCC kink at its finest: I'm the secured party, your wealth the collateral I tease.",
                "Subscribe for exclusive scenes where I dominate every clause."
            ],
            "suggestive": [
                "Exclusive content that blends power dynamics with financial insight.",
                "Premium access to sophisticated content with a twist."
            ]
        }
    }
    
    # Get appropriate template
    platform_templates = templates.get(platform, templates["FetLife"])
    tone_templates = platform_templates.get(tone, platform_templates["suggestive"])
    
    # Select a template (random in real implementation)
    import random
    base_content = random.choice(tone_templates)
    
    # Add topic customization if provided
    if topic != "general":
        content = f"{base_content} Focus: {topic}."
    else:
        content = base_content
    
    return content


@register_tool(
    name="generate_video",
    namespace="video",
    category=ToolCategory.CONTENT,
    description="Generates autonomous video content with AI-directed visuals and audio synthesis",
    parameters=[
        ToolParameter("topic", "string", True, "Topic or subject for video generation"),
        ToolParameter("scenes", "string", False, "JSON array of scene descriptions (optional)", "[]"),
        ToolParameter("style", "string", False, "Video style (intense, calm, corporate, neutral)", "neutral"),
        ToolParameter("output_filename", "string", False, "Output video filename", "output.mp4")
    ],
    return_description="Path to generated video file and production metadata",
    cost_tokens=500,
    guardrails=["Requires significant compute resources", "Long-running operation"]
)
def video_generation_tool(topic: str, scenes: str = "[]", style: str = "neutral", output_filename: str = "output.mp4") -> Dict[str, Any]:
    """
    Video generation tool using ZI Autonomous Video Pipeline
    Integrates AI-directed visuals, audio synthesis, and autonomous composition
    """
    try:
        import json
        import asyncio
        from ..video.video_pipeline import VideoPipeline, Scene, SceneDialogue, VideoStyle
        from ..memory.memory_manager import MemoryManager
        from ..guardrails.security_layer import SecurityLayer
        
        # Initialize ZI components
        memory_manager = MemoryManager()
        from ..guardrails.security_layer import TAKSHUN_CRITERIA
        security_layer = SecurityLayer(personalized_criteria=TAKSHUN_CRITERIA)
        pipeline = VideoPipeline(memory_manager, security_layer)
        
        # Parse scenes JSON if provided
        try:
            scenes_data = json.loads(scenes) if scenes else []
        except:
            scenes_data = []
        
        # Generate default scenes if none provided
        if not scenes_data:
            # Auto-generate scenes based on topic
            scenes_data = [
                {
                    "scene_id": 1,
                    "dialogue": [
                        {
                            "character": "Narrator", 
                            "dialogue": f"Welcome to this exploration of {topic}."
                        },
                        {
                            "character": "Agent",
                            "dialogue": f"The ZI Autonomous Agent System provides unique insights into {topic}."
                        }
                    ],
                    "style": style
                },
                {
                    "scene_id": 2,
                    "dialogue": [
                        {
                            "character": "Narrator",
                            "dialogue": f"Let's dive deeper into the implications of {topic}."
                        },
                        {
                            "character": "Agent", 
                            "dialogue": f"Our AI-driven analysis reveals fascinating patterns in {topic}."
                        }
                    ],
                    "style": style
                }
            ]
        
        # Convert to Scene objects
        scene_objects = []
        for scene_data in scenes_data:
            dialogue_objects = [
                SceneDialogue(
                    character=d["character"],
                    dialogue=d["dialogue"]
                )
                for d in scene_data["dialogue"]
            ]
            
            try:
                style_enum = VideoStyle(scene_data.get("style", style).lower())
            except ValueError:
                style_enum = VideoStyle.NEUTRAL
            
            scene_objects.append(Scene(
                scene_id=scene_data["scene_id"],
                dialogue=dialogue_objects,
                style=style_enum
            ))
        
        # Run async pipeline
        async def generate():
            return await pipeline.process_video_pipeline(scene_objects, output_filename)
        
        result = asyncio.run(generate())
        
        if result:
            metadata = pipeline.generate_metadata(topic)
            
            return {
                "success": True,
                "video_path": result,
                "metadata": {
                    "title": metadata.title,
                    "description": metadata.description,
                    "tags": metadata.tags
                },
                "scenes_processed": len(scene_objects),
                "production_time": "async_completed"
            }
        else:
            return {
                "success": False,
                "error": "Video generation failed",
                "details": "Check system logs for specific error information"
            }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "details": "Video pipeline encountered an error during execution"
        }


@register_tool(
    name="generate_content",
    namespace="content",
    category=ToolCategory.CONTENT,
    description="Generates platform-specific content with UCC commerce kinks and AIDA optimization",
    parameters=[
        ToolParameter("platform", "string", True, "Target platform (FetLife, Chaturbate, Fansly, Patreon)"),
        ToolParameter("tone", "string", True, "Content tone (suggestive, explicit, professional)"),
        ToolParameter("ucc_theme", "string", False, "UCC theme for kink integration", "secured_transaction")
    ],
    return_description="Generated content with AIDA optimization and UCC kink integration",
    cost_tokens=100
)
def content_generation_tool(platform: str, tone: str, ucc_theme: str = "secured_transaction") -> Dict[str, str]:
    """
    Content generation tool using FVCGen system
    """
    try:
        from ..content.fvcgen import ContentGenerator, Platform, Tone, UCCTheme
        
        generator = ContentGenerator()
        
        # Convert string parameters to enums
        try:
            platform_enum = Platform(platform.upper())
        except ValueError:
            platform_enum = Platform.FETLIFE
        
        try:
            tone_enum = Tone(tone.upper())
        except ValueError:
            tone_enum = Tone.EXPLICIT
        
        try:
            ucc_theme_enum = UCCTheme(ucc_theme.lower())
        except ValueError:
            ucc_theme_enum = UCCTheme.SECURED_TRANSACTION
        
        # Generate content
        result = generator.generate_content(
            platform=platform_enum,
            tone=tone_enum,
            ucc_theme=ucc_theme_enum,
            optimize_aida=True
        )
        
        return result
        
    except Exception as e:
        return {
            "error": str(e),
            "content": "Content generation failed. Please check platform and tone parameters."
        }


# Initialize the registry with example tools
def initialize_example_tools():
    """Register all example tools with the global registry"""
    # Tools are already registered via decorators
    # This function serves as a clear initialization point
    from .tool_registry import global_registry
    
    print(f"Registered {len(global_registry.list_all_tools())} example tools:")
    for tool_name in global_registry.list_all_tools():
        print(f"  - {tool_name}")


if __name__ == "__main__":
    initialize_example_tools()
