# ======================================================================================
# ZI AUTONOMOUS AGENT SYSTEM - VIRAL SOCIAL SHARING INTEGRATION
# ======================================================================================
# High-impact growth feature enabling one-click distribution across platforms
# Drives organic adoption through network effects and social proof
# ======================================================================================

import os
import json
import logging
import urllib.parse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import requests

# ======================================================================================
# PLATFORM ENUMERATIONS
# ======================================================================================

class SocialPlatform(Enum):
    """Supported social platforms for content distribution"""
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    REDDIT = "reddit"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"

class ContentFormat(Enum):
    """Content format optimizations per platform"""
    SHORT = "short"           # < 280 chars, hashtags
    MEDIUM = "medium"         # < 1000 chars, formatted
    LONG = "long"             # Full article/video
    STORY = "story"           # Vertical, visual
    THREAD = "thread"         # Multi-part content

# ======================================================================================
# DATA STRUCTURES
# ======================================================================================

@dataclass
class ShareableContent:
    """Content ready for social distribution"""
    title: str
    description: str
    content: str
    hashtags: List[str]
    media_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    call_to_action: str = ""
    
    def to_platform_format(self, platform: SocialPlatform) -> Dict:
        """Convert content to platform-specific format"""
        formats = {
            SocialPlatform.TWITTER: self._twitter_format,
            SocialPlatform.LINKEDIN: self._linkedin_format,
            SocialPlatform.FACEBOOK: self._facebook_format,
            SocialPlatform.REDDIT: self._reddit_format,
            SocialPlatform.INSTAGRAM: self._instagram_format,
            SocialPlatform.YOUTUBE: self._youtube_format,
        }
        
        formatter = formats.get(platform, self._generic_format)
        return formatter()
    
    def _twitter_format(self) -> Dict:
        """Twitter-optimized format"""
        hashtags_str = ' '.join([f"#{tag}" for tag in self.hashtags[:5]])
        content = f"{self.title}\n\n{self.description[:200]}...\n\n{hashtags_str}\n\n{self.call_to_action}"
        
        return {
            "text": content[:280],
            "media_url": self.media_url,
            "platform": "twitter"
        }
    
    def _linkedin_format(self) -> Dict:
        """LinkedIn-optimized format"""
        hashtags_str = ' '.join([f"#{tag.replace(' ', '')}" for tag in self.hashtags[:10]])
        content = f"{self.title}\n\n{self.description}\n\n{self.content[:500]}...\n\n{hashtags_str}\n\n{self.call_to_action}"
        
        return {
            "text": content,
            "media_url": self.media_url,
            "platform": "linkedin"
        }
    
    def _facebook_format(self) -> Dict:
        """Facebook-optimized format"""
        hashtags_str = ' '.join([f"#{tag}" for tag in self.hashtags[:10]])
        content = f"{self.title}\n\n{self.description}\n\n{self.content[:800]}...\n\n{hashtags_str}\n\n{self.call_to_action}"
        
        return {
            "text": content,
            "media_url": self.media_url,
            "thumbnail_url": self.thumbnail_url,
            "platform": "facebook"
        }
    
    def _reddit_format(self) -> Dict:
        """Reddit-optimized format"""
        content = f"{self.description}\n\n{self.content[:1000]}...\n\n{self.call_to_action}"
        
        return {
            "title": self.title,
            "text": content,
            "platform": "reddit"
        }
    
    def _instagram_format(self) -> Dict:
        """Instagram-optimized format"""
        hashtags_str = ' '.join([f"#{tag}" for tag in self.hashtags[:15]])
        content = f"{self.title}\n\n{self.description}\n\n{hashtags_str}"
        
        return {
            "caption": content,
            "media_url": self.media_url,
            "platform": "instagram"
        }
    
    def _youtube_format(self) -> Dict:
        """YouTube-optimized format"""
        hashtags_str = ', '.join([f"#{tag}" for tag in self.hashtags[:15]])
        content = f"{self.description}\n\n{self.content}\n\n{hashtags_str}\n\n{self.call_to_action}"
        
        return {
            "title": self.title,
            "description": content,
            "tags": self.hashtags[:15],
            "thumbnail_url": self.thumbnail_url,
            "platform": "youtube"
        }
    
    def _generic_format(self) -> Dict:
        """Generic format for other platforms"""
        return {
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "hashtags": self.hashtags,
            "media_url": self.media_url,
            "platform": "generic"
        }

@dataclass
class ShareResult:
    """Result of sharing operation"""
    success: bool
    platform: SocialPlatform
    post_url: Optional[str] = None
    engagement: Dict = None
    error_message: str = ""
    timestamp: str = ""

# ======================================================================================
# VIRAL SHARING ENGINE
# ======================================================================================

class ViralSharingEngine:
    """
    High-impact viral sharing engine for organic growth
    Enables one-click distribution with platform optimization
    """
    
    def __init__(self, firebase_url: Optional[str] = None):
        self.firebase_url = firebase_url or os.getenv("FIREBASE_URL")
        self.share_history = []
        
    def create_shareable_content(self, 
                                title: str,
                                description: str, 
                                content: str,
                                hashtags: List[str],
                                media_url: Optional[str] = None,
                                thumbnail_url: Optional[str] = None,
                                call_to_action: str = "Try it yourself!") -> ShareableContent:
        """Create shareable content object"""
        return ShareableContent(
            title=title,
            description=description,
            content=content,
            hashtags=hashtags,
            media_url=media_url,
            thumbnail_url=thumbnail_url,
            call_to_action=call_to_action
        )
    
    def generate_viral_content(self, 
                               topic: str,
                               content_type: str = "video",
                               platform: SocialPlatform = SocialPlatform.TWITTER) -> ShareableContent:
        """
        Auto-generate viral-optimized content using psychological triggers
        """
        # Viral title templates
        title_templates = [
            f"This AI {content_type} about {topic} will change everything 🔥",
            f"Nobody is talking about this {topic} {content_type} 🤯",
            f"I spent 100 hours building this {topic} system - here's what happened",
            f"The secret {topic} {content_type} experts don't want you to see",
            f"This {topic} {content_type} broke my algorithm 📈"
        ]
        
        # Viral description templates  
        description_templates = [
            f"Just discovered something incredible about {topic}. This changes everything we thought we knew.",
            f"After analyzing {topic} for months, I found patterns that shocked me.",
            f"The {topic} {content_type} industry is about to be disrupted. Here's why.",
            f"I reverse-engineered how {topic} actually works. You won't believe this."
        ]
        
        # Viral hashtags
        viral_hashtags = [
            topic.lower().replace(' ', ''),
            "ai", "artificialintelligence", 
            "tech", "innovation", "future",
            "viral", "trending", "mustwatch",
            "disruptive", "breakthrough"
        ]
        
        import random
        title = random.choice(title_templates)
        description = random.choice(description_templates)
        
        return self.create_shareable_content(
            title=title,
            description=description,
            content=f"Full {content_type} about {topic} with AI-powered analysis and insights.",
            hashtags=viral_hashtags,
            call_to_action="Link in bio - try it yourself!"
        )
    
    def generate_share_links(self, 
                           content: ShareableContent, 
                           base_url: str = "https://takshun-0024-14.web.app") -> Dict[SocialPlatform, str]:
        """
        Generate one-click share links for each platform
        """
        share_links = {}
        
        # Twitter
        twitter_text = urllib.parse.quote(content.to_platform_format(SocialPlatform.TWITTER)['text'])
        share_links[SocialPlatform.TWITTER] = f"https://twitter.com/intent/tweet?text={twitter_text}&url={base_url}"
        
        # LinkedIn
        linkedin_url = urllib.parse.quote(base_url)
        share_links[SocialPlatform.LINKEDIN] = f"https://www.linkedin.com/sharing/share-offsite/?url={linkedin_url}"
        
        # Facebook
        facebook_url = urllib.parse.quote(base_url)
        share_links[SocialPlatform.FACEBOOK] = f"https://www.facebook.com/sharer/sharer.php?u={facebook_url}"
        
        # Reddit
        reddit_title = urllib.parse.quote(content.title)
        reddit_url = urllib.parse.quote(base_url)
        share_links[SocialPlatform.REDDIT] = f"https://www.reddit.com/submit?url={reddit_url}&title={reddit_title}"
        
        # WhatsApp
        whatsapp_text = urllib.parse.quote(f"{content.title}\n{base_url}")
        share_links[SocialPlatform.WHATSAPP] = f"https://wa.me/?text={whatsapp_text}"
        
        # Telegram
        telegram_text = urllib.parse.quote(f"{content.title}\n{base_url}")
        share_links[SocialPlatform.TELEGRAM] = f"https://t.me/share/url?url={base_url}&text={telegram_text}"
        
        return share_links
    
    def track_share(self, 
                   platform: SocialPlatform, 
                   content_type: str,
                   success: bool = True,
                   post_url: Optional[str] = None):
        """Track sharing analytics for optimization"""
        share_event = {
            "platform": platform.value,
            "content_type": content_type,
            "success": success,
            "post_url": post_url,
            "timestamp": __import__('time').time()
        }
        
        self.share_history.append(share_event)
        
        # Log to Firebase
        if self.firebase_url:
            try:
                requests.post(f"{self.firebase_url}/share_analytics.json", json=share_event)
            except Exception as e:
                logging.warning(f"Firebase logging failed: {e}")
    
    def get_viral_score(self, content: ShareableContent) -> float:
        """
        Calculate viral potential score based on psychological triggers
        Higher score = higher viral potential
        """
        score = 0.0
        
        # Title length (optimal: 50-100 chars)
        title_len = len(content.title)
        if 50 <= title_len <= 100:
            score += 20
        elif 40 <= title_len <= 120:
            score += 10
        
        # Viral trigger words
        viral_words = ["secret", "shocking", "broke", "nobody", "experts", "disrupt", "change", "breakthrough"]
        title_lower = content.title.lower()
        score += sum(10 for word in viral_words if word in title_lower)
        
        # Hashtag optimization (5-15 hashtags)
        if 5 <= len(content.hashtags) <= 15:
            score += 15
        elif 3 <= len(content.hashtags) <= 20:
            score += 5
        
        # Call to action presence
        if content.call_to_action:
            score += 10
        
        # Question marks (create curiosity)
        score += content.title.count('?') * 5
        
        # Numbers (add specificity)
        import re
        if re.search(r'\d+', content.title):
            score += 5
        
        return min(score, 100)  # Cap at 100
    
    def optimize_for_virality(self, content: ShareableContent) -> ShareableContent:
        """
        Auto-optimize content for maximum viral potential
        """
        # Add viral trigger words to title
        viral_prefixes = ["🔥", "🤯", "📈", "💡"]
        import random
        if not any(emoji in content.title for emoji in viral_prefixes):
            content.title = f"{random.choice(viral_prefixes)} {content.title}"
        
        # Optimize hashtag count
        if len(content.hashtags) < 5:
            additional_tags = ["viral", "trending", "mustsee", "innovation", "ai"]
            content.hashtags.extend(additional_tags[: (10 - len(content.hashtags))])
        elif len(content.hashtags) > 20:
            content.hashtags = content.hashtags[:20]
        
        # Add call to action if missing
        if not content.call_to_action:
            content.call_to_action = "Try it yourself - link in bio!"
        
        return content
    
    def create_viral_campaign(self,
                             topic: str,
                             platforms: List[SocialPlatform],
                             content_type: str = "video") -> Dict[SocialPlatform, Dict]:
        """
        Create a coordinated viral campaign across multiple platforms
        """
        campaign = {}
        base_content = self.generate_viral_content(topic, content_type)
        
        for platform in platforms:
            platform_content = base_content.to_platform_format(platform)
            share_links = self.generate_share_links(base_content)
            viral_score = self.get_viral_score(base_content)
            
            campaign[platform] = {
                "content": platform_content,
                "share_link": share_links.get(platform),
                "viral_score": viral_score,
                "optimized": viral_score > 70
            }
        
        return campaign

# ======================================================================================
# GROWTH ANALYTICS
# ======================================================================================

class GrowthAnalytics:
    """
    Analytics engine for tracking growth metrics and optimizing strategy
    """
    
    def __init__(self, firebase_url: Optional[str] = None):
        self.firebase_url = firebase_url or os.getenv("FIREBASE_URL")
        self.metrics = {
            "total_shares": 0,
            "platform_breakdown": {},
            "viral_content": [],
            "best_performing_topics": [],
            "growth_rate": 0.0
        }
    
    def track_growth_event(self, event_type: str, data: Dict):
        """Track growth-related events"""
        event = {
            "event_type": event_type,
            "data": data,
            "timestamp": __import__('time').time()
        }
        
        if self.firebase_url:
            try:
                requests.post(f"{self.firebase_url}/growth_events.json", json=event)
            except Exception as e:
                logging.warning(f"Firebase logging failed: {e}")
    
    def calculate_viral_coefficient(self) -> float:
        """
        Calculate viral coefficient (k-factor)
        k = (number of shares per user) × (conversion rate of shares)
        """
        # This would be calculated from actual analytics data
        # For now, return a placeholder
        return 1.2  # k > 1 indicates viral growth
    
    def recommend_growth_strategy(self) -> List[str]:
        """
        Recommend growth strategies based on current metrics
        """
        strategies = [
            "Focus on Twitter/X for tech-savvy audience",
            "Create LinkedIn content for professional reach",
            "Optimize YouTube metadata for search discovery",
            "Engage with Reddit communities for authentic discussions",
            "Use Instagram Stories for behind-the-scenes content",
            "Leverage WhatsApp groups for direct sharing",
            "Create shareable templates for easy distribution",
            "Implement referral incentives for user growth"
        ]
        
        return strategies

# ======================================================================================
# REFERRAL SYSTEM
# ======================================================================================

class ReferralSystem:
    """
    Viral referral system for organic user acquisition
    """
    
    def __init__(self):
        self.referral_codes = {}
        self.referral_rewards = {
            "referrer": {"premium_features": 7, "api_calls": 1000},
            "referee": {"premium_features": 3, "api_calls": 500}
        }
    
    def generate_referral_code(self, user_id: str) -> str:
        """Generate unique referral code for user"""
        import hashlib
        import random
        
        code = f"ZI-{user_id[:4].upper()}-{random.randint(1000, 9999)}"
        self.referral_codes[code] = {
            "user_id": user_id,
            "uses": 0,
            "created_at": __import__('time').time()
        }
        return code
    
    def track_referral(self, referral_code: str, new_user_id: str) -> bool:
        """Track successful referral and distribute rewards"""
        if referral_code not in self.referral_codes:
            return False
        
        # Mark referral as used
        self.referral_codes[referral_code]["uses"] += 1
        
        # Distribute rewards (would integrate with user system)
        return True
    
    def get_referral_link(self, referral_code: str, base_url: str = "https://takshun-0024-14.web.app") -> str:
        """Generate referral link with tracking"""
        return f"{base_url}?ref={referral_code}"

# ======================================================================================
# UTILITY FUNCTIONS
# ======================================================================================

def create_viral_launch_strategy(topic: str) -> Dict:
    """
    Create a complete viral launch strategy for new content
    """
    sharing_engine = ViralSharingEngine()
    
    # Generate viral content
    viral_content = sharing_engine.generate_viral_content(topic, "video")
    
    # Optimize for virality
    optimized_content = sharing_engine.optimize_for_virality(viral_content)
    
    # Create campaign across platforms
    platforms = [
        SocialPlatform.TWITTER,
        SocialPlatform.LINKEDIN, 
        SocialPlatform.FACEBOOK,
        SocialPlatform.REDDIT
    ]
    
    campaign = sharing_engine.create_viral_campaign(topic, platforms, "video")
    
    # Generate share links
    share_links = sharing_engine.generate_share_links(optimized_content)
    
    return {
        "content": optimized_content,
        "campaign": campaign,
        "share_links": share_links,
        "viral_score": sharing_engine.get_viral_score(optimized_content),
        "platforms": platforms
    }

# ======================================================================================
# ENTRY POINT
# ======================================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test viral sharing engine
    sharing_engine = ViralSharingEngine()
    
    # Create viral content
    viral_content = sharing_engine.generate_viral_content("AI Autonomous Systems", "video")
    
    print("🚀 Viral Content Generated:")
    print(f"Title: {viral_content.title}")
    print(f"Description: {viral_content.description}")
    print(f"Hashtags: {', '.join(viral_content.hashtags)}")
    print(f"Viral Score: {sharing_engine.get_viral_score(viral_content)}")
    
    # Generate share links
    share_links = sharing_engine.generate_share_links(viral_content)
    print("\n📱 Share Links:")
    for platform, link in share_links.items():
        print(f"{platform.value}: {link}")
    
    # Create viral campaign
    campaign = sharing_engine.create_viral_campaign("AI Systems", [SocialPlatform.TWITTER, SocialPlatform.LINKEDIN])
    print("\n🎯 Viral Campaign Created:")
    for platform, data in campaign.items():
        print(f"{platform.value}: Score {data['viral_score']}, Optimized: {data['optimized']}")