# ======================================================================================
# ZI AUTONOMOUS AGENT SYSTEM - PUBLIC API ENDPOINT
# ======================================================================================
# High-impact growth feature enabling ecosystem expansion
# Public API allows third-party developers to build on the platform
# ======================================================================================

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.security import APIKeyHeader
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import logging
from datetime import datetime, timedelta
import json
import uuid

# Import existing systems
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))

from video.video_pipeline import VideoPipeline
from memory.memory_manager import MemoryManager
from guardrails.security_layer import SecurityLayer, TAKSHUN_CRITERIA
from template_marketplace import TemplateMarketplace, TemplateCategory
from seo_optimizer import SEOOptimizerEngine

# ======================================================================================
# API MODELS
# ======================================================================================

class VideoGenerationRequest(BaseModel):
    topic: str = Field(..., description="Topic for video generation")
    style: str = Field("neutral", description="Visual style (intense, calm, corporate, neutral)")
    scenes: Optional[str] = Field(None, description="JSON array of scene descriptions")
    output_filename: str = Field("output.mp4", description="Output filename")

class ContentGenerationRequest(BaseModel):
    platform: str = Field(..., description="Target platform")
    tone: str = Field("professional", description="Content tone")
    topic: str = Field(..., description="Content topic")
    optimize_seo: bool = Field(True, description="Apply SEO optimization")

class TemplateInstantiationRequest(BaseModel):
    template_id: str = Field(..., description="Template ID to instantiate")
    customizations: Dict[str, Any] = Field(default_factory=dict, description="User customizations")

class SEOOptimizationRequest(BaseModel):
    title: str = Field(..., description="Content title")
    description: str = Field(..., description="Content description")
    content: str = Field(..., description="Main content")
    content_type: str = Field("article", description="Content type (article, video, software)")

class APIResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: str
    features: List[str]

# ======================================================================================
# API INITIALIZATION
# ======================================================================================

app = FastAPI(
    title="ZI Autonomous Agent System API",
    description="Public API for ecosystem expansion and third-party integrations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# API Key security (simplified for demo)
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Depends(API_KEY_HEADER)):
    """Validate API key"""
    if api_key == "demo-key-123":  # In production, use proper auth
        return api_key
    raise HTTPException(status_code=403, detail="Invalid API Key")

# Initialize systems
memory_manager = MemoryManager()
security_layer = SecurityLayer(personalized_criteria=TAKSHUN_CRITERIA)
video_pipeline = VideoPipeline(memory_manager, security_layer)
template_marketplace = TemplateMarketplace()
seo_optimizer = SEOOptimizerEngine()

# ======================================================================================
# RATE LIMITING (SIMPLIFIED)
# ======================================================================================

class RateLimiter:
    def __init__(self):
        self.requests = {}
        self.rate_limit = 100  # requests per hour
    
    def check_rate_limit(self, api_key: str) -> bool:
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        
        if api_key not in self.requests:
            self.requests[api_key] = []
        
        # Remove old requests
        self.requests[api_key] = [
            req_time for req_time in self.requests[api_key]
            if req_time > hour_ago
        ]
        
        if len(self.requests[api_key]) >= self.rate_limit:
            return False
        
        self.requests[api_key].append(now)
        return True

rate_limiter = RateLimiter()

# ======================================================================================
# ENDPOINTS
# ======================================================================================

@app.get("/", response_model=HealthResponse)
async def root():
    """API health check and feature overview"""
    uptime = str(datetime.now() - datetime(2024, 1, 1))  # Simplified uptime
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        uptime=uptime,
        features=[
            "video_generation",
            "content_generation", 
            "template_marketplace",
            "seo_optimization",
            "analytics_tracking"
        ]
    )

@app.post("/api/v1/video/generate", response_model=APIResponse)
async def generate_video(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key)
):
    """Generate AI video with given parameters"""
    if not rate_limiter.check_rate_limit(api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    try:
        # This would trigger the video pipeline in background
        task_id = str(uuid.uuid4())
        
        # In production, this would be a background job
        result = {
            "task_id": task_id,
            "status": "processing",
            "estimated_time": "5-10 minutes",
            "topic": request.topic,
            "style": request.style
        }
        
        return APIResponse(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.post("/api/v1/content/generate", response_model=APIResponse)
async def generate_content(
    request: ContentGenerationRequest,
    api_key: str = Depends(get_api_key)
):
    """Generate platform-optimized content"""
    if not rate_limiter.check_rate_limit(api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    try:
        from tools.example_tools import content_generation_tool
        
        result = content_generation_tool(
            platform=request.platform,
            tone=request.tone,
            ucc_theme="secured_transaction"
        )
        
        if request.optimize_seo:
            # Apply SEO optimization
            optimized = seo_optimizer.optimize_content(
                title=result.get("title", request.topic),
                description=result.get("description", ""),
                content=result.get("content", "")
            )
            result["seo_optimized"] = {
                "title": optimized.title,
                "description": optimized.description,
                "tags": optimized.tags
            }
        
        return APIResponse(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/api/v1/templates", response_model=APIResponse)
async def list_templates(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    api_key: str = Depends(get_api_key)
):
    """List available templates with filters"""
    if not rate_limiter.check_rate_limit(api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    try:
        # Convert string filters to enums
        category_filter = None
        if category:
            try:
                category_filter = TemplateCategory(category.lower())
            except ValueError:
                pass
        
        templates = template_marketplace.search_templates(
            query=search or "",
            category=category_filter,
            difficulty=None  # Simplified
        )
        
        result = {
            "count": len(templates),
            "templates": [t.to_dict() for t in templates]
        }
        
        return APIResponse(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.post("/api/v1/templates/instantiate", response_model=APIResponse)
async def instantiate_template(
    request: TemplateInstantiationRequest,
    api_key: str = Depends(get_api_key)
):
    """Instantiate a template with customizations"""
    if not rate_limiter.check_rate_limit(api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    try:
        instance = template_marketplace.instantiate_template(
            template_id=request.template_id,
            user_id=api_key,  # Simplified user identification
            customizations=request.customizations
        )
        
        result = {
            "instance_id": str(uuid.uuid4()),
            "template_id": request.template_id,
            "customizations": request.customizations,
            "created_at": instance.created_at
        }
        
        return APIResponse(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.post("/api/v1/seo/optimize", response_model=APIResponse)
async def optimize_content_seo(
    request: SEOOptimizationRequest,
    api_key: str = Depends(get_api_key)
):
    """Optimize content for SEO"""
    if not rate_limiter.check_rate_limit(api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    try:
        optimized = seo_optimizer.optimize_content(
            title=request.title,
            description=request.description,
            content=request.content,
            content_type=request.content_type
        )
        
        result = {
            "optimized_title": optimized.title,
            "optimized_description": optimized.description,
            "tags": optimized.tags,
            "canonical_url": optimized.canonical_url,
            "schema_markup": optimized.schema_markup,
            "meta_tags": optimized.meta_tags,
            "seo_score": optimized.seo_score.overall_score
        }
        
        return APIResponse(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/api/v1/analytics/overview", response_model=APIResponse)
async def get_analytics_overview(api_key: str = Depends(get_api_key)):
    """Get analytics overview for API usage"""
    if not rate_limiter.check_rate_limit(api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    try:
        # Simplified analytics (would integrate with Firebase in production)
        result = {
            "api_calls_today": len(rate_limiter.requests.get(api_key, [])),
            "rate_limit_remaining": rate_limiter.rate_limit - len(rate_limiter.requests.get(api_key, [])),
            "popular_endpoints": {
                "video_generation": 45,
                "content_generation": 30,
                "template_usage": 25
            },
            "success_rate": 98.5
        }
        
        return APIResponse(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

# ======================================================================================
# ENTRY POINT
# ======================================================================================

if __name__ == "__main__":
    import uvicorn
    
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 Starting ZI Autonomous Agent System Public API...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔑 Demo API Key: demo-key-123")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)