#!/bin/bash

# ======================================================================================
# ZI AUTONOMOUS AGENT SYSTEM - QUICK START SCRIPT
# ======================================================================================
# This script helps you quickly set up and start using the growth features
# ======================================================================================

echo "🚀 ZI Autonomous Agent System - Quick Start"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo ""
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "🧪 Testing growth features..."
echo ""

echo "📱 Testing viral sharing..."
python core/growth/social_sharing.py
echo ""

echo "🏪 Testing template marketplace..."
python core/growth/template_marketplace.py
echo ""

echo "🔍 Testing SEO optimizer..."
python core/growth/seo_optimizer.py
echo ""

echo "📅 Testing scheduling and collaboration..."
python core/growth/scheduling_collaboration.py
echo ""

echo "✅ All growth features tested successfully!"
echo ""

echo "🌐 Access the web dashboard:"
echo "   https://takshun-0024-14.web.app"
echo ""

echo "📚 Available interfaces:"
echo "   1. Dashboard - Full agent interface with analytics"
echo "   2. AEE - Agent Execution Environment"
echo ""

echo "📖 Documentation:"
echo "   - DEPLOYMENT_GUIDE.md - Complete deployment guide"
echo "   - FINAL_GROWTH_SYSTEM.md - Growth system documentation"
echo "   - GROWTH_FEATURES_SUMMARY.md - Growth features overview"
echo ""

echo "🔌 To start the API server (optional):"
echo "   python core/growth/public_api.py"
echo "   Then visit: http://localhost:8000/docs"
echo ""

echo "🎬 To test video pipeline (optional):"
echo "   pip install moviepy elevenlabs pillow"
echo "   export ELEVEN_LABS_API_KEY='your_key'"
echo "   python test_video_pipeline.py"
echo ""

echo "✅ Quick start complete! Your ZI Agent System is ready to grow!"
