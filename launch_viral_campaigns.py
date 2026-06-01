#!/usr/bin/env python3
"""
Multi-platform viral campaign launcher for ZI Autonomous Agent System
Creates and deploys multiple viral campaigns for maximum reach and growth
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.growth import ViralSharingEngine, create_viral_launch_strategy
import json

def main():
    print("🚀 MULTI-PLATFORM VIRAL CAMPAIGN LAUNCHER")
    print("=" * 70)
    print()
    
    # Initialize viral sharing engine
    sharing_engine = ViralSharingEngine()
    
    # Create multiple viral campaigns for different audiences
    campaigns = []
    
    # Campaign 1: For developers/tech community
    print("📱 Creating Campaign 1: Developer/Tech Community")
    campaign1 = create_viral_launch_strategy("AI Autonomous Agents for Developers")
    campaigns.append({
        "audience": "Developer/Tech Community",
        "campaign": campaign1,
        "platforms": ["twitter", "linkedin", "reddit"]
    })
    print(f"   Title: {campaign1['content'].title}")
    print(f"   Viral Score: {campaign1['viral_score']}")
    print()
    
    # Campaign 2: For business/productivity
    print("📱 Creating Campaign 2: Business/Productivity")
    campaign2 = create_viral_launch_strategy("AI Automation for Business")
    campaigns.append({
        "audience": "Business/Productivity",
        "campaign": campaign2,
        "platforms": ["linkedin", "facebook", "twitter"]
    })
    print(f"   Title: {campaign2['content'].title}")
    print(f"   Viral Score: {campaign2['viral_score']}")
    print()
    
    # Campaign 3: For creators/content
    print("📱 Creating Campaign 3: Content Creators")
    campaign3 = create_viral_launch_strategy("AI Video Production Tools")
    campaigns.append({
        "audience": "Content Creators",
        "campaign": campaign3,
        "platforms": ["twitter", "instagram", "tiktok", "whatsapp"]
    })
    print(f"   Title: {campaign3['content'].title}")
    print(f"   Viral Score: {campaign3['viral_score']}")
    print()
    
    # Campaign 4: For general AI enthusiasts
    print("📱 Creating Campaign 4: General AI Enthusiasts")
    campaign4 = create_viral_launch_strategy("The Future of AI Systems")
    campaigns.append({
        "audience": "General AI Enthusiasts",
        "campaign": campaign4,
        "platforms": ["twitter", "linkedin", "reddit", "telegram"]
    })
    print(f"   Title: {campaign4['content'].title}")
    print(f"   Viral Score: {campaign4['viral_score']}")
    print()
    
    print("🎯 CAMPAIGN OVERVIEW")
    print("-" * 50)
    print(f"Total Campaigns: {len(campaigns)}")
    print(f"Target Audiences: {[c['audience'] for c in campaigns]}")
    print(f"Total Platform Links: {sum(len(c['campaign']['share_links']) for c in campaigns)}")
    print()
    
    print("🔗 SHARE LINKS (ONE-CLICK DISTRIBUTION)")
    print("=" * 50)
    
    for i, campaign_data in enumerate(campaigns, 1):
        print(f"\n📱 CAMPAIGN {i}: {campaign_data['audience'].upper()}")
        print("-" * 50)
        
        for platform in campaign_data['platforms']:
            if platform in campaign_data['campaign']['share_links']:
                link = campaign_data['campaign']['share_links'][platform]
                print(f"{platform.value.upper()}: {link}")
        
        print()
    
    print("📊 CAMPAIGN PERFORMANCE ANALYSIS")
    print("-" * 50)
    
    total_viral_score = sum(c['campaign']['viral_score'] for c in campaigns)
    avg_viral_score = total_viral_score / len(campaigns)
    
    print(f"Average Viral Score: {avg_viral_score:.1f}/100")
    print(f"Total Viral Potential: {total_viral_score:.1f}")
    print(f"Campaign Coverage: {len(set(p for c in campaigns for p in c['platforms']))} platforms")
    print()
    
    print("🎯 DEPLOYMENT STRATEGY")
    print("-" * 50)
    print("1. **Immediate**: Share all campaign links across respective platforms")
    print("2. **Timing**: Post during optimal hours (9-11 AM, 5-7 PM local time)")
    print("3. **Sequencing**: Stagger posts by 30-60 minutes for algorithmic benefit")
    print("4. **Engagement**: Respond to comments and engage with shares")
    print("5. **Monitoring**: Track performance in dashboard Analytics tab")
    print()
    
    print("📈 EXPECTED IMPACT")
    print("-" * 50)
    print(f"Total Share Links: {sum(len(c['campaign']['share_links']) for c in campaigns)}")
    print(f"Projected Shares: {len(campaigns) * 20}-{len(campaigns) * 50} (per campaign)")
    print(f"Projected Reach: {len(campaigns) * 500}-{len(campaigns) * 2000} users")
    print(f"Projected Sign-ups: {len(campaigns) * 50}-{len(campaigns) * 200} users")
    print()
    
    print("🔔 AUTOMATION OPPORTUNITIES")
    print("-" * 50)
    print("• Set up recurring campaigns using scheduling system")
    print("• A/B test different viral content variations")
    print("• Automate posting times based on platform analytics")
    print("• Create campaign templates for quick deployment")
    print("• Set up monitoring alerts for viral threshold triggers")
    print()
    
    # Save campaign data for automation
    campaign_data_export = {
        "campaigns": [
            {
                "audience": c['audience'],
                "title": c['campaign']['content'].title,
                "description": c['campaign']['content'].description,
                "hashtags": c['campaign']['content'].hashtags,
                "viral_score": c['campaign']['viral_score'],
                "platforms": [p.value if hasattr(p, 'value') else str(p) for p in c['platforms']],
                "share_links": {str(k): v for k, v in c['campaign']['share_links'].items()}
            }
            for c in campaigns
        ],
        "total_campaigns": len(campaigns),
        "average_viral_score": avg_viral_score,
        "deployment_date": "2026-06-01",
        "dashboard_url": "https://takshun-0024-14.web.app"
    }
    
    with open('viral_campaigns_export.json', 'w') as f:
        json.dump(campaign_data_export, f, indent=2)
    
    print("💾 Campaign data exported to: viral_campaigns_export.json")
    print()
    
    print("✅ MULTI-PLATFORM VIRAL CAMPAIGNS READY FOR DEPLOYMENT!")
    print()
    print("🎯 IMMEDIATE ACTIONS:")
    print("• Click share links above to post each campaign")
    print("• Monitor performance in dashboard Analytics tab")
    print("• Engage with responses and comments")
    print("• Scale successful content patterns")
    print("• Schedule recurring campaigns using automation")

if __name__ == "__main__":
    main()