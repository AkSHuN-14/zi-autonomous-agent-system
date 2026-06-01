# 🚀 ZI Autonomous Agent System - Deployment Guide

## 📋 Prerequisites

### For Web Dashboard (Already Deployed)
✅ **Live on Firebase Hosting**: https://takshun-0024-14.web.app
- No additional setup required
- Access immediately in browser

### For API Server Deployment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start API server
python core/growth/public_api.py
```

API Documentation: http://localhost:8000/docs
Demo API Key: `demo-key-123`

### For Video Pipeline (Optional)
```bash
# Install media dependencies
pip install moviepy elevenlabs pillow imageio

# Set API keys
export ELEVEN_LABS_API_KEY="your_key"
export OPENAI_API_KEY="your_key"
export FIREBASE_URL="your_firebase_url"

# Install FFmpeg (required for MoviePy)
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

---

## 🎯 Quick Start Guide

### 1. Access Web Dashboard
1. Open https://takshun-0024-14.web.app
2. Choose your interface:
   - **Dashboard** (default) - Full agent interface with growth analytics
   - **AEE** - Agent Execution Environment for YAML testing

### 2. Use Growth Features

#### 🎬 Video Production
1. Click "Video" tab in dashboard
2. Enter topic and select style
3. Click "Generate AI Video"
4. Monitor progress and view results

#### 📊 View Analytics
1. Click "Analytics" tab in dashboard
2. View:
   - Viral coefficient (k-factor)
   - Platform performance breakdown
   - Top performing content
   - Growth insights and recommendations

#### 🔥 Share Content Virally
```python
from core.growth import ViralSharingEngine, create_viral_launch_strategy

# Create viral campaign
campaign = create_viral_launch_strategy("AI Automation")
# Returns share links for all platforms
```

#### 🏪 Use Templates
```python
from core.growth import TemplateMarketplace

marketplace = TemplateMarketplace()
templates = marketplace.search_templates(query="video")
# Instantiate for instant results
```

#### 🔍 Optimize SEO
```python
from core.growth import SEOOptimizerEngine

optimizer = SEOOptimizerEngine()
optimized = optimizer.optimize_content(title, description, content)
# Returns SEO-optimized content with schema markup
```

#### 👥 Collaborate with Teams
```python
from core.growth import CollaborationSystem

collaboration = CollaborationSystem()
workspace = collaboration.create_workspace("My Team", "user123")
invite = collaboration.invite_to_workspace(workspace.id, "user123")
# Share templates and content with team
```

#### 📅 Schedule Content
```python
from core.growth import ContentSchedulingSystem

scheduler = ContentSchedulingSystem()
scheduled = scheduler.schedule_content("video", "AI Tips", "multi")
calendar = scheduler.generate_content_calendar(weeks=4)
# Automated content calendar generation
```

---

## 🔌 API Usage

### Start API Server
```bash
# Activate virtual environment first
source venv/bin/activate

# Start server
python core/growth/public_api.py
```

### API Endpoints

#### Generate Video
```bash
curl -X POST "http://localhost:8000/api/v1/video/generate" \
  -H "X-API-Key: demo-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI Automation",
    "style": "corporate",
    "output_filename": "ai_automation.mp4"
  }'
```

#### Generate Content
```bash
curl -X POST "http://localhost:8000/api/v1/content/generate" \
  -H "X-API-Key: demo-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "twitter",
    "tone": "professional",
    "topic": "AI tips",
    "optimize_seo": true
  }'
```

#### List Templates
```bash
curl -X GET "http://localhost:8000/api/v1/templates?category=video_production" \
  -H "X-API-Key: demo-key-123"
```

#### Optimize SEO
```bash
curl -X POST "http://localhost:8000/api/v1/seo/optimize" \
  -H "X-API-Key: demo-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI Guide",
    "description": "Learn AI automation",
    "content": "Full content here...",
    "content_type": "article"
  }'
```

### Full API Documentation
Interactive docs available at: http://localhost:8000/docs

---

## 🧪 Testing

### Run Growth Feature Tests
```bash
# Test viral sharing
python core/growth/social_sharing.py

# Test template marketplace
python core/growth/template_marketplace.py

# Test SEO optimizer
python core/growth/seo_optimizer.py

# Test scheduling and collaboration
python core/growth/scheduling_collaboration.py
```

### Run Video Pipeline Tests
```bash
# Basic test (no dependencies required)
python test_video_pipeline.py

# Full render test (requires MoviePy + API keys)
python test_video_pipeline.py --full-render
```

---

## 📊 Monitoring & Analytics

### Firebase Console
- **Project**: https://console.firebase.google.com/project/takshun-0024-14/overview
- **Features**: Realtime Database, Hosting, Analytics
- **Logs**: All growth events logged to Firebase

### Dashboard Analytics
Access via: https://takshun-0024-14.web.app → Analytics Tab
- Real-time performance metrics
- Platform breakdown
- Growth insights
- Viral coefficient tracking

---

## 🔧 Configuration

### Environment Variables
```bash
# Required for video pipeline
export ELEVEN_LABS_API_KEY="your_key"
export OPENAI_API_KEY="your_key"
export FIREBASE_URL="your_firebase_url"

# Optional for SEO tools
export GOOGLE_TRENDS_API_KEY="your_key"

# Optional for stock footage
export PEXELS_API_KEY="your_key"
```

### Firebase Configuration
Edit `config/settings.yaml`:
```yaml
agent:
  max_iterations: 50
  error_threshold: 3
  max_context_tokens: 2000

growth:
  firebase_url: "your_firebase_url"
  rate_limit: 100

video:
  resolution: [1280, 720]
  fps: 24
  threads: 4
```

---

## 🚀 Production Deployment

### Option 1: Firebase Hosting (Current)
✅ **Already Deployed**: https://takshun-0024-14.web.app
- Static web hosting
- Global CDN
- Automatic SSL
- Zero configuration

### Option 2: Cloud Deployment (API Server)
```bash
# Deploy to cloud platform (AWS, GCP, DigitalOcean)
# Use Docker for containerization

# Build Docker image
docker build -t zi-agent-system .

# Run container
docker run -p 8000:8000 -e FIREBASE_URL="your_url" zi-agent-system
```

### Option 3: Serverless Functions
- Deploy API endpoints to Cloud Functions
- Scale automatically
- Pay-per-use pricing

---

## 📈 Growth Strategy Implementation

### Week 1: Foundation
1. ✅ Deploy web dashboard (done)
2. ✅ Test all growth features (done)
3. 📝 Create and share viral content
4. 📝 Optimize existing content for SEO

### Week 2: Content Distribution
1. 📝 Generate viral content using social sharing
2. 📝 Publish to template marketplace
3. 📝 Schedule recurring content calendar
4. 📝 Set up team collaboration workspace

### Week 3: Ecosystem Expansion
1. 📝 Deploy public API server
2. 📝 Create developer documentation
3. 📝 Reach out to potential third-party developers
4. 📝 Set up API analytics and monitoring

### Week 4: Optimization
1. 📝 Analyze growth metrics from dashboard
2. 📝 Optimize top-performing content
3. 📝 Scale successful templates
4. 📝 Refine growth strategy based on data

---

## 🎯 Success Metrics

### Key Performance Indicators
- **Viral Coefficient**: Target k > 2.0
- **Organic Traffic Share**: Target > 70%
- **User Retention**: Target > 85% (30-day)
- **Template Adoption**: Target > 60% (new users)
- **API Ecosystem**: Target > 200 integrations

### Track These Metrics
- Dashboard analytics (real-time)
- Firebase console (event logs)
- API analytics (usage statistics)
- SEO rankings (search console)

---

## 🆘 Troubleshooting

### Common Issues

**Dashboard shows blank screen**
- Clear browser cache
- Try different browser
- Check internet connection

**Video generation fails**
- Install MoviePy: `pip install moviepy`
- Install FFmpeg: `brew install ffmpeg` (macOS)
- Set API keys properly

**API server won't start**
- Create virtual environment
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 availability

**SEO optimization errors**
- Ensure content has sufficient length
- Check title/description length
- Verify keyword density

---

## 🔐 Security

### API Keys
- Never commit API keys to git
- Use environment variables
- Rotate keys regularly
- Use different keys for development/production

### Firebase Security Rules
- Update rules in Firebase Console
- Enable authentication for production
- Set up proper read/write permissions

### Rate Limiting
- API server has 100 requests/hour limit per key
- Monitor usage in Firebase analytics
- Adjust limits as needed

---

## 📚 Additional Resources

### Documentation
- `GROWTH_FEATURES_SUMMARY.md` - Initial growth features overview
- `FINAL_GROWTH_SYSTEM.md` - Complete growth system documentation
- `VIDEO_PIPELINE_INTEGRATION.md` - Video pipeline integration guide

### Source Code
- `core/growth/` - All growth feature implementations
- `core/video/` - Video production pipeline
- `ui/web/` - Web dashboard interfaces

### External Links
- Firebase Console: https://console.firebase.google.com/project/takshun-0024-14/overview
- Live Dashboard: https://takshun-0024-14.web.app

---

## 🎉 You're Ready!

Your ZI Autonomous Agent System is now equipped with:

✅ **Production-ready growth engine** with 8 high-impact features
✅ **Live web dashboard** with analytics and video production
✅ **Complete API system** ready for ecosystem expansion
✅ **Comprehensive documentation** for deployment and usage

**Next Steps**:
1. Access the dashboard: https://takshun-0024-14.web.app
2. Explore the Analytics tab to see growth metrics
3. Try the Video Production features
4. Deploy the API server for third-party integrations
5. Start creating viral content and watch your system grow!

**System Status**: 🌟 **Production-Ready Growth Engine**
**Deployment**: ✅ **Live and Operational**
**Growth Potential**: 🚀 **Unlimited**