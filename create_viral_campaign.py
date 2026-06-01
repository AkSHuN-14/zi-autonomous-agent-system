#!/usr/bin/env python3
"""
Initial viral campaign demonstration for ZI Autonomous Agent System
Creates viral content and generates share links for immediate distribution
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.growth import ViralSharingEngine, create_viral_launch_strategy

def main():
    print("🚀 Creating Initial Viral Campaign for ZI Autonomous Agent System")
    print("=" * 70)
    print()
    
    # Initialize viral sharing engine
    sharing_engine = ViralSharingEngine()
    
    # Create viral campaign for the system itself
    campaign = create_viral_launch_strategy("AI Autonomous Systems")
    
    print("📱 VIRAL CONTENT GENERATED:")
    print("-" * 50)
    print(f"Title: {campaign['content'].title}")
    print(f"Description: {campaign['content'].description}")
    print(f"Hashtags: {', '.join(campaign['content'].hashtags[:5])}")
    print(f"Viral Score: {campaign['viral_score']}")
    print()
    
    print("🔗 SHARE LINKS (ONE-CLICK DISTRIBUTION):")
    print("-" * 50)
    for platform, link in campaign['share_links'].items():
        print(f"{platform.value.upper()}: {link}")
    print()
    
    print("📊 CAMPAIGN PERFORMANCE BY PLATFORM:")
    print("-" * 50)
    for platform, data in campaign['campaign'].items():
        print(f"{platform.value.upper()}:")
        print(f"  Viral Score: {data['viral_score']}")
        print(f"  Optimized: {'✅ Yes' if data['optimized'] else '❌ No'}")
        print()
    
    print("🎯 CAMPAIGN INSIGHTS:")
    print("-" * 50)
    print("• Highest viral potential on Twitter/X")
    print("• LinkedIn good for professional audience")
    print("• Multi-platform approach maximizes reach")
    print("• Share links are ready for immediate distribution")
    print()
    
    print("📈 NEXT STEPS:")
    print("-" * 50)
    print("1. Share the viral content across all platforms")
    print("2. Monitor analytics in dashboard (Analytics tab)")
    print("3. Optimize based on platform performance")
    print("4. Create recurring viral campaigns using scheduling")
    print()
    
    print("🌟 ACCESS YOUR DASHBOARD:")
    print("https://takshun-0024-14.web.app")
    print()
    
    print("✅ Viral campaign ready for deployment!")
    print()
    print("📋 QUICK ACTIONS:")
    print("• Click any share link above to post content")
    print("• Visit dashboard to track performance")
    print("• Use templates to create more viral content")
    print("• Schedule recurring content for automation")

if __name__ == "__main__":
    main()
