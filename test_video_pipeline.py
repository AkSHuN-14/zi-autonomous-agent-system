"""
Test script for ZI Autonomous Video Pipeline
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
from core.video.video_pipeline import VideoPipeline, Scene, SceneDialogue, VideoStyle
from core.memory.memory_manager import MemoryManager
from core.guardrails.security_layer import SecurityLayer

def test_video_pipeline():
    """Test the video pipeline with sample data"""
    
    print("🎬 Testing ZI Autonomous Video Pipeline")
    print("=" * 50)
    
    # Initialize components
    memory_manager = MemoryManager()
    from core.guardrails.security_layer import TAKSHUN_CRITERIA
    security_layer = SecurityLayer(personalized_criteria=TAKSHUN_CRITERIA)
    pipeline = VideoPipeline(memory_manager, security_layer)
    
    # Create test scenes
    scenes = [
        Scene(
            scene_id=1,
            dialogue=[
                SceneDialogue(
                    character="Narrator",
                    dialogue="The ZI Autonomous Agent System represents a breakthrough in AI architecture."
                ),
                SceneDialogue(
                    character="Agent", 
                    dialogue="Our ReAct-based agent loop enables self-correction and autonomous decision-making."
                )
            ],
            style=VideoStyle.CORPORATE
        ),
        Scene(
            scene_id=2,
            dialogue=[
                SceneDialogue(
                    character="Narrator",
                    dialogue="The system features parallel processing and fault isolation for reliability."
                ),
                SceneDialogue(
                    character="Agent",
                    dialogue="This achieves production-grade scalability and performance."
                )
            ],
            style=VideoStyle.NEUTRAL
        )
    ]
    
    print(f"Created {len(scenes)} test scenes")
    print(f"Scene 1: {len(scenes[0].dialogue)} dialogue lines")
    print(f"Scene 2: {len(scenes[1].dialogue)} dialogue lines")
    
    # Test AI Director
    print("\n🧠 Testing AI Director")
    test_dialogues = [
        "This is an intense battle scene",
        "A calm peaceful moment",
        "Corporate business strategy",
        "Just a neutral explanation"
    ]
    
    for dialogue in test_dialogues:
        style = pipeline.ai_director(dialogue)
        print(f"  '{dialogue}' -> {style.value}")
    
    # Test metadata generation
    print("\n📋 Testing Metadata Generation")
    metadata = pipeline.generate_metadata("AI Finance Systems")
    print(f"  Title: {metadata.title}")
    print(f"  Description: {metadata.description}")
    print(f"  Tags: {', '.join(metadata.tags)}")
    
    # Test profit calculation
    print("\n💰 Testing Profit Calculation")
    from core.video.video_pipeline import VideoPerformance
    
    test_performance = VideoPerformance(
        views=5000,
        watch_time=300.0,
        avg_duration=60.0,
        revenue=25.0
    )
    
    score = pipeline.calculate_profit_score(test_performance)
    decision = pipeline.scaling_decision(test_performance)
    
    print(f"  Views: {test_performance.views}")
    print(f"  Revenue: ${test_performance.revenue}")
    print(f"  Profit Score: {score:.2f}")
    print(f"  Scaling Decision: {decision}")
    
    print("\n✅ All tests completed successfully!")
    print("\n📝 Note: Full video rendering requires:")
    print("   - MoviePy installation")
    print("   - ElevenLabs API key")
    print("   - FFmpeg system installation")
    print("\nTo test full pipeline:")
    print("   pip install moviepy elevenlabs")
    print("   export ELEVEN_LABS_API_KEY='your_key'")
    print("   python test_video_pipeline.py --full-render")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--full-render":
        print("🎬 Running full video render test...")
        print("⚠️  This requires complete dependencies and API keys")
        print("⚠️  Make sure to install: pip install moviepy elevenlabs pillow")
        
        async def full_render_test():
            memory_manager = MemoryManager()
            from core.guardrails.security_layer import TAKSHUN_CRITERIA
            security_layer = SecurityLayer(personalized_criteria=TAKSHUN_CRITERIA)
            pipeline = VideoPipeline(memory_manager, security_layer)
            
            scenes = [
                Scene(
                    scene_id=1,
                    dialogue=[SceneDialogue(character="Narrator", dialogue="Testing the ZI video pipeline")],
                    style=VideoStyle.NEUTRAL
                )
            ]
            
            result = await pipeline.process_video_pipeline(scenes, "test_output.mp4")
            if result:
                print(f"✅ Video created: {result}")
            else:
                print("❌ Video creation failed")
        
        asyncio.run(full_render_test())
    else:
        test_video_pipeline()