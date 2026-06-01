# ======================================================================================
# ZI AUTONOMOUS AGENT SYSTEM - TEMPLATE MARKETPLACE
# ======================================================================================
# High-impact growth feature providing instant value through pre-built configurations
# Drives adoption by reducing time-to-value and enabling instant results
# ======================================================================================

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import hashlib

# ======================================================================================
# TEMPLATE CATEGORIES
# ======================================================================================

class TemplateCategory(Enum):
    """Template categories for different use cases"""
    VIDEO_PRODUCTION = "video_production"
    CONTENT_GENERATION = "content_generation"
    AGENT_WORKFLOWS = "agent_workflows"
    DATA_ANALYSIS = "data_analysis"
    BUSINESS_AUTOMATION = "business_automation"
    SOCIAL_MEDIA = "social_media"
    DEVELOPER_TOOLS = "developer_tools"
    MARKETING = "marketing"

class TemplateDifficulty(Enum):
    """Difficulty levels for templates"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

# ======================================================================================
# DATA STRUCTURES
# ======================================================================================

@dataclass
class TemplateConfig:
    """Configuration for a template"""
    name: str
    description: str
    category: TemplateCategory
    difficulty: TemplateDifficulty
    config: Dict[str, Any]
    estimated_time: str  # e.g., "5 minutes", "1 hour"
    features: List[str]
    requirements: List[str]
    author: str = "ZI Team"
    version: str = "1.0"
    tags: List[str] = None
    usage_count: int = 0
    rating: float = 0.0
    created_at: str = ""
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert template to dictionary"""
        return asdict(self)
    
    def generate_hash(self) -> str:
        """Generate unique hash for template identification"""
        config_str = json.dumps(self.config, sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()[:8]

@dataclass
class TemplateInstance:
    """Instance of a template with user customization"""
    template_id: str
    user_customizations: Dict[str, Any]
    created_at: str = ""
    status: str = "active"
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

# ======================================================================================
# TEMPLATE MARKETPLACE
# ======================================================================================

class TemplateMarketplace:
    """
    Template marketplace for instant value delivery
    Pre-built configurations that users can instantly deploy
    """
    
    def __init__(self):
        self.templates: Dict[str, TemplateConfig] = {}
        self.user_instances: Dict[str, List[TemplateInstance]] = {}
        self._initialize_builtin_templates()
    
    def _initialize_builtin_templates(self):
        """Initialize built-in templates for instant value"""
        
        # Video Production Templates
        self.register_template(TemplateConfig(
            name="Quick Explainer Video",
            description="Generate engaging explainer videos in minutes with AI-directed visuals",
            category=TemplateCategory.VIDEO_PRODUCTION,
            difficulty=TemplateDifficulty.BEGINNER,
            config={
                "style": "neutral",
                "duration": "60-120",
                "voice_type": "professional",
                "scenes": [
                    {"type": "intro", "duration": "10"},
                    {"type": "content", "duration": "40"},
                    {"type": "outro", "duration": "10"}
                ],
                "music": "upbeat",
                "text_overlay": True
            },
            estimated_time="5 minutes",
            features=[
                "Auto-generate script from topic",
                "AI-directed visual style",
                "Professional voice synthesis",
                "One-click rendering"
            ],
            requirements=["ElevenLabs API key"],
            tags=["video", "explainer", "quick", "ai"]
        ))
        
        self.register_template(TemplateConfig(
            name="Viral Short-Form Video",
            description="Create TikTok/Instagram-style vertical videos optimized for engagement",
            category=TemplateCategory.VIDEO_PRODUCTION,
            difficulty=TemplateDifficulty.INTERMEDIATE,
            config={
                "style": "intense",
                "duration": "15-60",
                "aspect_ratio": "9:16",
                "voice_type": "energetic",
                "music": "trending",
                "text_overlay": True,
                "caption_style": "bold"
            },
            estimated_time="10 minutes",
            features=[
                "Vertical video format",
                "Trending audio integration",
                "Bold caption overlays",
                "Platform optimization"
            ],
            requirements=["ElevenLabs API key", "Trending music library"],
            tags=["video", "viral", "shorts", "tiktok", "instagram"]
        ))
        
        # Content Generation Templates
        self.register_template(TemplateConfig(
            name="SEO Blog Post Generator",
            description="Generate SEO-optimized blog posts with keyword integration",
            category=TemplateCategory.CONTENT_GENERATION,
            difficulty=TemplateDifficulty.BEGINNER,
            config={
                "word_count": "1000-1500",
                "tone": "professional",
                "keyword_density": "1-2%",
                "heading_structure": True,
                "meta_description": True,
                "internal_linking": False
            },
            estimated_time="2 minutes",
            features=[
                "Keyword optimization",
                "Readability scoring",
                "Meta tag generation",
                "Heading hierarchy"
            ],
            requirements=["OpenAI API key"],
            tags=["content", "seo", "blog", "writing"]
        ))
        
        self.register_template(TemplateConfig(
            name="Social Media Content Pack",
            description="Generate a week's worth of social media content in one click",
            category=TemplateCategory.SOCIAL_MEDIA,
            difficulty=TemplateDifficulty.BEGINNER,
            config={
                "platforms": ["twitter", "linkedin", "instagram", "facebook"],
                "posts_per_platform": 7,
                "content_types": ["educational", "promotional", "engagement"],
                "hashtag_sets": True,
                "scheduling_suggestions": True
            },
            estimated_time="3 minutes",
            features=[
                "Multi-platform content",
                "Hashtag optimization",
                "Posting schedule",
                "Engagement prompts"
            ],
            requirements=["OpenAI API key"],
            tags=["social", "marketing", "content", "automation"]
        ))
        
        # Agent Workflow Templates
        self.register_template(TemplateConfig(
            name="Research Assistant Workflow",
            description="Automated research agent that gathers, analyzes, and summarizes information",
            category=TemplateCategory.AGENT_WORKFLOWS,
            difficulty=TemplateDifficulty.INTERMEDIATE,
            config={
                "search_sources": ["web", "academic", "news"],
                "analysis_depth": "comprehensive",
                "output_format": "structured_report",
                "citation_style": "apa",
                "max_sources": 10
            },
            estimated_time="15 minutes",
            features=[
                "Multi-source search",
                "Automated citation",
                "Structured reporting",
                "Fact verification"
            ],
            requirements=["Web search API", "OpenAI API key"],
            tags=["agent", "research", "automation", "workflow"]
        ))
        
        self.register_template(TemplateConfig(
            name="Customer Support Agent",
            description="Intelligent customer support agent with knowledge base integration",
            category=TemplateCategory.AGENT_WORKFLOWS,
            difficulty=TemplateDifficulty.ADVANCED,
            config={
                "knowledge_base": "custom",
                "response_style": "professional",
                "escalation_rules": True,
                "sentiment_analysis": True,
                "multi_language": False
            },
            estimated_time="30 minutes",
            features=[
                "Knowledge base integration",
                "Sentiment-aware responses",
                "Automatic escalation",
                "Conversation memory"
            ],
            requirements=["Vector database", "OpenAI API key"],
            tags=["agent", "support", "customer", "automation"]
        ))
        
        # Business Automation Templates
        self.register_template(TemplateConfig(
            name="Email Campaign Automation",
            description="Automated email campaign system with personalization and scheduling",
            category=TemplateCategory.BUSINESS_AUTOMATION,
            difficulty=TemplateDifficulty.INTERMEDIATE,
            config={
                "email_types": ["welcome", "newsletter", "promotional"],
                "personalization_level": "high",
                "a_b_testing": True,
                "scheduling": "optimized",
                "tracking": True
            },
            estimated_time="20 minutes",
            features=[
                "Dynamic personalization",
                "A/B testing framework",
                "Optimal send timing",
                "Performance tracking"
            ],
            requirements=["Email service API", "OpenAI API key"],
            tags=["automation", "email", "marketing", "business"]
        ))
        
        # Data Analysis Templates
        self.register_template(TemplateConfig(
            name="Financial Data Analyzer",
            description="Automated financial data analysis with insights and predictions",
            category=TemplateCategory.DATA_ANALYSIS,
            difficulty=TemplateDifficulty.ADVANCED,
            config={
                "data_sources": ["csv", "api", "database"],
                "analysis_types": ["trends", "anomalies", "predictions"],
                "visualization": True,
                "report_generation": True,
                "alert_thresholds": True
            },
            estimated_time="25 minutes",
            features=[
                "Trend detection",
                "Anomaly identification",
                "Predictive modeling",
                "Automated reporting"
            ],
            requirements=["Data access", "OpenAI API key"],
            tags=["data", "finance", "analysis", "automation"]
        ))
        
        # Developer Tools Templates
        self.register_template(TemplateConfig(
            name="Code Review Assistant",
            description="AI-powered code review with security analysis and optimization suggestions",
            category=TemplateCategory.DEVELOPER_TOOLS,
            difficulty=TemplateDifficulty.INTERMEDIATE,
            config={
                "languages": ["python", "javascript", "java", "go"],
                "review_depth": "comprehensive",
                "security_analysis": True,
                "performance_optimization": True,
                "documentation_suggestions": True
            },
            estimated_time="10 minutes",
            features=[
                "Multi-language support",
                "Security vulnerability detection",
                "Performance optimization",
                "Documentation generation"
            ],
            requirements=["Repository access", "OpenAI API key"],
            tags=["developer", "code", "review", "automation"]
        ))
        
        # Marketing Templates
        self.register_template(TemplateConfig(
            name="Marketing Campaign Generator",
            description="Generate complete marketing campaigns with copy, visuals, and strategy",
            category=TemplateCategory.MARKETING,
            difficulty=TemplateDifficulty.INTERMEDIATE,
            config={
                "campaign_types": ["product_launch", "brand_awareness", "lead_generation"],
                "content_variants": 3,
                "a_b_testing": True,
                "channel_strategy": True,
                "budget_optimization": True
            },
            estimated_time="15 minutes",
            features=[
                "Multi-variant content",
                "Channel-specific optimization",
                "A/B testing setup",
                "Budget allocation"
            ],
            requirements=["OpenAI API key", "Marketing platform APIs"],
            tags=["marketing", "campaign", "automation", "growth"]
        ))
    
    def register_template(self, template: TemplateConfig) -> str:
        """Register a new template in the marketplace"""
        template_id = template.generate_hash()
        self.templates[template_id] = template
        return template_id
    
    def get_template(self, template_id: str) -> Optional[TemplateConfig]:
        """Get template by ID"""
        return self.templates.get(template_id)
    
    def search_templates(self, 
                        query: str = "",
                        category: Optional[TemplateCategory] = None,
                        difficulty: Optional[TemplateDifficulty] = None,
                        tags: Optional[List[str]] = None) -> List[TemplateConfig]:
        """Search templates with filters"""
        results = []
        
        for template in self.templates.values():
            # Text search
            if query and query.lower() not in template.name.lower() and query.lower() not in template.description.lower():
                continue
            
            # Category filter
            if category and template.category != category:
                continue
            
            # Difficulty filter
            if difficulty and template.difficulty != difficulty:
                continue
            
            # Tags filter
            if tags and not any(tag in template.tags for tag in tags):
                continue
            
            results.append(template)
        
        # Sort by usage count and rating
        results.sort(key=lambda t: (t.usage_count, t.rating), reverse=True)
        
        return results
    
    def get_popular_templates(self, limit: int = 10) -> List[TemplateConfig]:
        """Get most popular templates"""
        sorted_templates = sorted(
            self.templates.values(),
            key=lambda t: t.usage_count,
            reverse=True
        )
        return sorted_templates[:limit]
    
    def get_templates_by_category(self, category: TemplateCategory) -> List[TemplateConfig]:
        """Get templates by category"""
        return [t for t in self.templates.values() if t.category == category]
    
    def instantiate_template(self, 
                           template_id: str,
                           user_id: str,
                           customizations: Dict[str, Any]) -> TemplateInstance:
        """Create a user instance of a template with customizations"""
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Increment usage count
        template.usage_count += 1
        
        # Create instance
        instance = TemplateInstance(
            template_id=template_id,
            user_customizations=customizations
        )
        
        # Track instance
        if user_id not in self.user_instances:
            self.user_instances[user_id] = []
        self.user_instances[user_id].append(instance)
        
        return instance
    
    def get_user_instances(self, user_id: str) -> List[TemplateInstance]:
        """Get all template instances for a user"""
        return self.user_instances.get(user_id, [])
    
    def rate_template(self, template_id: str, rating: float) -> bool:
        """Rate a template (1.0 - 5.0)"""
        template = self.get_template(template_id)
        if not template:
            return False
        
        if not 1.0 <= rating <= 5.0:
            return False
        
        # Simple average calculation (in production, would track individual ratings)
        template.rating = (template.rating + rating) / 2
        return True
    
    def get_quick_start_templates(self) -> List[TemplateConfig]:
        """Get templates best for quick start (beginner, high rating)"""
        return [
            t for t in self.templates.values()
            if t.difficulty == TemplateDifficulty.BEGINNER and t.rating >= 4.0
        ]

# ======================================================================================
# TEMPLATE RECOMMENDATION ENGINE
# ======================================================================================

class TemplateRecommendationEngine:
    """
    AI-powered template recommendation engine
    Suggests templates based on user behavior and goals
    """
    
    def __init__(self, marketplace: TemplateMarketplace):
        self.marketplace = marketplace
    
    def recommend_for_goal(self, goal: str) -> List[TemplateConfig]:
        """Recommend templates based on user goal"""
        goal_mapping = {
            "create_content": [TemplateCategory.CONTENT_GENERATION, TemplateCategory.SOCIAL_MEDIA],
            "automate_work": [TemplateCategory.AGENT_WORKFLOWS, TemplateCategory.BUSINESS_AUTOMATION],
            "analyze_data": [TemplateCategory.DATA_ANALYSIS],
            "generate_videos": [TemplateCategory.VIDEO_PRODUCTION],
            "grow_business": [TemplateCategory.MARKETING, TemplateCategory.SOCIAL_MEDIA],
            "develop_software": [TemplateCategory.DEVELOPER_TOOLS]
        }
        
        categories = goal_mapping.get(goal.lower(), [])
        if not categories:
            return self.marketplace.get_popular_templates(5)
        
        recommendations = []
        for category in categories:
            recommendations.extend(self.marketplace.get_templates_by_category(category))
        
        return sorted(recommendations, key=lambda t: t.rating, reverse=True)[:5]
    
    def recommend_for_skill_level(self, skill_level: str) -> List[TemplateConfig]:
        """Recommend templates based on user skill level"""
        skill_mapping = {
            "beginner": TemplateDifficulty.BEGINNER,
            "intermediate": TemplateDifficulty.INTERMEDIATE,
            "advanced": TemplateDifficulty.ADVANCED
        }
        
        difficulty = skill_mapping.get(skill_level.lower(), TemplateDifficulty.BEGINNER)
        
        matching_templates = [
            t for t in self.marketplace.templates.values()
            if t.difficulty == difficulty or t.difficulty == TemplateDifficulty.BEGINNER
        ]
        
        return sorted(matching_templates, key=lambda t: t.rating, reverse=True)[:5]

# ======================================================================================
# ENTRY POINT
# ======================================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize marketplace
    marketplace = TemplateMarketplace()
    
    print(f"🏪 Template Marketplace initialized with {len(marketplace.templates)} templates")
    
    # Search templates
    print("\n🔍 Search results for 'video':")
    video_templates = marketplace.search_templates(query="video")
    for template in video_templates:
        print(f"  - {template.name} ({template.difficulty.value})")
    
    # Get popular templates
    print("\n🔥 Popular templates:")
    popular = marketplace.get_popular_templates(3)
    for template in popular:
        print(f"  - {template.name} (Used: {template.usage_count} times, Rating: {template.rating:.1f})")
    
    # Get templates by category
    print("\n📂 Content Generation templates:")
    content_templates = marketplace.get_templates_by_category(TemplateCategory.CONTENT_GENERATION)
    for template in content_templates:
        print(f"  - {template.name}")
    
    # Recommendation engine
    recommender = TemplateRecommendationEngine(marketplace)
    
    print("\n💡 Recommendations for 'create_content' goal:")
    recommendations = recommender.recommend_for_goal("create_content")
    for template in recommendations:
        print(f"  - {template.name}")