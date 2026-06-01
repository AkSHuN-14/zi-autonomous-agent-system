# ======================================================================================
# ZI AUTONOMOUS AGENT SYSTEM - VIDEO PRODUCTION PIPELINE
# ======================================================================================
# Integrated video composition system with:
# - Parallel execution and fault tolerance
# - Scene-level isolation
# - Memory-safe rendering
# - Audio synchronization
# - Firebase logging integration
# - Profit-aware optimization
# ======================================================================================

import os
import asyncio
import logging
import json
import requests
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# Video processing imports (with proper error handling)
try:
    from moviepy.editor import (
        VideoFileClip,
        AudioFileClip,
        CompositeAudioClip,
        concatenate_videoclips,
        concatenate_audioclips,
        ColorClip,
        CompositeVideoClip
    )
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    logging.warning("MoviePy not available - video pipeline will use mock mode")

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL not available - text rendering will use fallback")

# ZI Agent System imports
from memory.memory_manager import MemoryManager
from guardrails.security_layer import SecurityLayer

# ======================================================================================
# CONFIGURATION
# ======================================================================================
VIDEO_RESOLUTION = (1280, 720)
FPS = 24
THREADS = 4
BASE_DIR = "./runtime/video"

# ======================================================================================
# DATA STRUCTURES
# ======================================================================================

class VideoStyle(Enum):
    INTENSE = "intense"
    CALM = "calm"
    CORPORATE = "corporate"
    NEUTRAL = "neutral"

@dataclass
class SceneDialogue:
    character: str
    dialogue: str
    voice_id: Optional[str] = None

@dataclass
class Scene:
    scene_id: int
    dialogue: List[SceneDialogue]
    style: VideoStyle = VideoStyle.NEUTRAL

@dataclass
class VideoMetadata:
    title: str
    description: str
    tags: List[str]
    category: str = "22"

@dataclass
class VideoPerformance:
    views: int
    watch_time: float
    avg_duration: float
    revenue: float

# ======================================================================================
# VIDEO PIPELINE CLASS
# ======================================================================================

class VideoPipeline:
    """
    ZI Autonomous Agent Video Production Pipeline
    Integrated with the ZI agent system for autonomous media generation
    """
    
    def __init__(self, memory_manager: MemoryManager, security_layer: SecurityLayer):
        self.memory_manager = memory_manager
        self.security_layer = security_layer
        self.firebase_url = os.getenv("FIREBASE_URL")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
        
        # Get user_id from personalized criteria if available
        self.user_id = getattr(security_layer.personalized_criteria, 'user_id', 'UNKNOWN') if security_layer.personalized_criteria else 'UNKNOWN'
        
        # Voice mapping for TA'K$HUN personalization
        self.voice_map = {
            "Narrator": os.getenv("NARRATOR_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"),
            "Agent": os.getenv("AGENT_VOICE_ID", "AZnzlk1XvdvUeBnXmlld")
        }
        
        self._setup_directories()
        
    def _setup_directories(self):
        """Create necessary directories for video production"""
        directories = [
            BASE_DIR,
            os.path.join(BASE_DIR, "audio"),
            os.path.join(BASE_DIR, "video"),
            os.path.join(BASE_DIR, "output"),
            os.path.join(BASE_DIR, "thumbnails")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def log_event(self, event: Dict):
        """Log events to Firebase for monitoring and analytics"""
        if self.firebase_url:
            try:
                requests.post(f"{self.firebase_url}/video_logs.json", json=event)
            except Exception as e:
                logging.warning(f"Firebase logging failed: {e}")
        
        # Also log to memory manager
        self.memory_manager.add_observation(f"Video Pipeline: {event}")
    
    def ai_director(self, dialogue_text: str) -> VideoStyle:
        """
        AI Director - Analyze dialogue and determine visual style
        Can be upgraded to use LLM for more sophisticated analysis
        """
        text = dialogue_text.lower()
        
        if any(word in text for word in ["war", "fight", "battle", "conflict"]):
            return VideoStyle.INTENSE
        elif any(word in text for word in ["love", "peace", "calm", "gentle"]):
            return VideoStyle.CALM
        elif any(word in text for word in ["money", "power", "business", "corporate"]):
            return VideoStyle.CORPORATE
        else:
            return VideoStyle.NEUTRAL
    
    def generate_audio(self, text: str, voice_id: str, output_path: str) -> bool:
        """
        Generate audio using ElevenLabs API
        Returns True if successful, False otherwise
        """
        if not self.eleven_labs_api_key:
            logging.warning("ElevenLabs API key not set - using mock audio")
            return self._generate_mock_audio(output_path)
        
        try:
            from elevenlabs.client import ElevenLabs
            client = ElevenLabs(api_key=self.eleven_labs_api_key)
            
            audio_stream = client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2"
            )
            
            with open(output_path, "wb") as f:
                for chunk in audio_stream:
                    f.write(chunk)
            
            return True
        except Exception as e:
            logging.error(f"Audio generation failed: {e}")
            return self._generate_mock_audio(output_path)
    
    def _generate_mock_audio(self, output_path: str) -> bool:
        """Generate mock audio for testing when API is unavailable"""
        try:
            # Create a silent audio file as placeholder
            if MOVIEPY_AVAILABLE:
                from moviepy.editor import AudioFileClip
                silent = AudioFileClip("core/video/assets/silence.mp3") if os.path.exists("core/video/assets/silence.mp3") else None
                if silent:
                    silent.write_audiofile(output_path)
                    return True
        except Exception as e:
            logging.warning(f"Mock audio generation failed: {e}")
        
        # Create empty file as fallback
        with open(output_path, 'wb') as f:
            f.write(b'')
        return False
    
    def create_text_overlay(self, text: str, duration: float) -> Optional['VideoFileClip']:
        """
        Create text overlay using PIL rendering (more stable than TextClip)
        """
        if not PIL_AVAILABLE or not MOVIEPY_AVAILABLE:
            return None
        
        try:
            img = Image.new("RGB", VIDEO_RESOLUTION, (0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            # Wrap text to fit width
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                if draw.textlength(' '.join(current_line), font=font) > VIDEO_RESOLUTION[0] * 0.8:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw text
            y_position = VIDEO_RESOLUTION[1] - 150
            for line in reversed(lines):
                draw.text((50, y_position), line, fill="white", font=font)
                y_position -= 50
            
            temp_path = os.path.join(BASE_DIR, "temp_text.png")
            img.save(temp_path)
            
            clip = VideoFileClip(temp_path).set_duration(duration)
            os.remove(temp_path)
            
            return clip
        except Exception as e:
            logging.error(f"Text overlay creation failed: {e}")
            return None
    
    def process_scene(self, scene: Scene) -> Optional[str]:
        """
        Process a single scene: generate audio, create video, composite
        Returns path to rendered scene video
        """
        scene_id = scene.scene_id
        audio_dir = os.path.join(BASE_DIR, "audio")
        video_dir = os.path.join(BASE_DIR, "video")
        
        clips = []
        
        for i, dialogue in enumerate(scene.dialogue):
            if not dialogue.dialogue:
                continue
            
            # Get voice ID
            voice_id = self.voice_map.get(dialogue.character)
            if not voice_id:
                logging.warning(f"No voice ID for character: {dialogue.character}")
                continue
            
            # Generate audio
            audio_path = os.path.join(audio_dir, f"scene_{scene_id}_{i}.mp3")
            success = self.generate_audio(dialogue.dialogue, voice_id, audio_path)
            
            if not success or not os.path.exists(audio_path):
                continue
            
            # Load audio
            if MOVIEPY_AVAILABLE:
                try:
                    audio = AudioFileClip(audio_path)
                    duration = audio.duration
                except Exception as e:
                    logging.error(f"Failed to load audio: {e}")
                    continue
            else:
                duration = 3.0  # Mock duration
            
            # AI Director decision for visual style
            style = self.ai_director(dialogue.dialogue)
            
            # Create background based on style
            if MOVIEPY_AVAILABLE:
                color_map = {
                    VideoStyle.INTENSE: (50, 0, 0),
                    VideoStyle.CALM: (0, 0, 50),
                    VideoStyle.CORPORATE: (30, 30, 30),
                    VideoStyle.NEUTRAL: (0, 0, 0)
                }
                
                bg_color = color_map.get(style, (0, 0, 0))
                video = ColorClip(size=VIDEO_RESOLUTION, color=bg_color, duration=duration)
                video = video.set_audio(audio)
                
                # Add text overlay
                text_overlay = self.create_text_overlay(dialogue.dialogue, duration)
                if text_overlay:
                    final_clip = CompositeVideoClip([video, text_overlay])
                else:
                    final_clip = video
                
                clips.append(final_clip)
            
            self.log_event({
                "stage": "dialogue_processed",
                "scene": scene_id,
                "line": i,
                "style": style.value,
                "character": dialogue.character
            })
        
        if not clips:
            logging.warning(f"No clips generated for scene {scene_id}")
            return None
        
        # Concatenate scene clips
        if MOVIEPY_AVAILABLE:
            try:
                scene_video = concatenate_videoclips(clips, method="compose")
                output_path = os.path.join(video_dir, f"scene_{scene_id}.mp4")
                
                scene_video.write_videofile(
                    output_path,
                    fps=FPS,
                    threads=THREADS,
                    codec='libx264',
                    audio_codec='aac'
                )
                
                self.log_event({
                    "stage": "scene_complete",
                    "scene": scene_id,
                    "output": output_path
                })
                
                return output_path
            except Exception as e:
                logging.error(f"Scene composition failed: {e}")
                return None
        
        return None
    
    def compose_final_video(self, scene_paths: List[str], output_path: str, music_path: Optional[str] = None) -> Optional[str]:
        """
        Compose final video from rendered scenes
        """
        if not MOVIEPY_AVAILABLE:
            logging.warning("MoviePy not available - skipping final composition")
            return None
        
        valid_paths = [p for p in scene_paths if p and os.path.exists(p)]
        
        if not valid_paths:
            logging.warning("No valid scene paths for final composition")
            return None
        
        try:
            clips = [VideoFileClip(p) for p in valid_paths]
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Add background music if provided
            if music_path and os.path.exists(music_path):
                try:
                    music = AudioFileClip(music_path).volumex(0.1)
                    music = music.loop(duration=final_video.duration)
                    final_audio = CompositeAudioClip([final_video.audio, music])
                    final_video = final_video.set_audio(final_audio)
                except Exception as e:
                    logging.warning(f"Failed to add music: {e}")
            
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                threads=THREADS
            )
            
            self.log_event({
                "stage": "final_complete",
                "output": output_path,
                "scenes_composed": len(valid_paths)
            })
            
            return output_path
        except Exception as e:
            logging.error(f"Final composition failed: {e}")
            return None
    
    async def process_video_pipeline(self, scenes: List[Scene], output_filename: str = "final.mp4") -> Optional[str]:
        """
        Main async pipeline - processes scenes in parallel
        """
        self.log_event({"stage": "pipeline_start", "scene_count": len(scenes)})
        
        # Process scenes in parallel
        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            scene_futures = [
                executor.submit(self.process_scene, scene)
                for scene in scenes
            ]
            scene_paths = [f.result() for f in scene_futures]
        
        # Compose final video
        output_path = os.path.join(BASE_DIR, "output", output_filename)
        final_video = self.compose_final_video(scene_paths, output_path)
        
        if final_video:
            self.log_event({"stage": "pipeline_complete", "output": final_video})
        
        return final_video
    
    def generate_metadata(self, topic: str) -> VideoMetadata:
        """
        Generate optimized metadata for video
        Can be upgraded with LLM for more sophisticated metadata
        """
        return VideoMetadata(
            title=f"🔥 {topic} EXPOSED",
            description=f"This reveals the hidden truth about {topic} that changes everything.",
            tags=["ai", "autonomous", "intelligence", topic, "exposed"],
            category="22"  # People & Blogs
        )
    
    def calculate_profit_score(self, performance: VideoPerformance) -> float:
        """
        Calculate profit-weighted performance score
        Used for autonomous scaling decisions
        """
        if not performance:
            return 0.0
        
        # Weighted formula: views + watch_time + revenue_multiplier
        score = (performance.views * 0.3) + (performance.watch_time * 0.4) + (performance.revenue * 100)
        return score
    
    def scaling_decision(self, performance: VideoPerformance) -> str:
        """
        Make autonomous scaling decision based on performance
        """
        score = self.calculate_profit_score(performance)
        
        if score > 10000:
            return "scale_aggressively"
        elif score > 3000:
            return "scale_moderately"
        elif score > 1000:
            return "maintain"
        else:
            return "kill"

# ======================================================================================
# UTILITY FUNCTIONS
# ======================================================================================

def create_sample_scenes() -> List[Scene]:
    """Create sample scenes for testing"""
    return [
        Scene(
            scene_id=1,
            dialogue=[
                SceneDialogue(
                    character="Narrator",
                    dialogue="The ZI Autonomous Agent System represents a breakthrough in artificial intelligence architecture."
                ),
                SceneDialogue(
                    character="Agent",
                    dialogue="Our ReAct-based agent loop with structured YAML outputs enables self-correction and autonomous decision-making."
                )
            ],
            style=VideoStyle.CORPORATE
        ),
        Scene(
            scene_id=2,
            dialogue=[
                SceneDialogue(
                    character="Narrator",
                    dialogue="The system features memory management, tool orchestration, and personalized security protocols."
                ),
                SceneDialogue(
                    character="Agent",
                    dialogue="With parallel execution and fault isolation, we achieve production-grade reliability and scalability."
                )
            ],
            style=VideoStyle.NEUTRAL
        )
    ]

# ======================================================================================
# ENTRY POINT
# ======================================================================================

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from core.memory.memory_manager import MemoryManager
    from core.guardrails.security_layer import SecurityLayer
    
    logging.basicConfig(level=logging.INFO)
    
    # Initialize ZI agent components
    memory_manager = MemoryManager()
    security_layer = SecurityLayer(user_id="TA'K$HUN")
    
    # Create video pipeline
    pipeline = VideoPipeline(memory_manager, security_layer)
    
    # Create sample scenes
    scenes = create_sample_scenes()
    
    # Run pipeline
    async def main():
        result = await pipeline.process_video_pipeline(scenes, "zi_agent_demo.mp4")
        if result:
            logging.info(f"Video successfully created: {result}")
        else:
            logging.error("Video creation failed")
    
    asyncio.run(main())