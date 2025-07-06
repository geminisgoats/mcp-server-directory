import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Sample MCP servers for marketing/SEO
sample_servers = [
    {
        "id": "1",
        "name": "SEO Master Pro",
        "description": "Advanced SEO analytics and optimization MCP server for comprehensive website analysis",
        "detailed_description": "SEO Master Pro is a comprehensive MCP server that provides advanced SEO analytics, keyword research, competitor analysis, and optimization recommendations. It integrates with major search engines and provides real-time insights to improve your website's search rankings.",
        "category": "SEO Analytics",
        "features": [
            "Real-time SEO scoring",
            "Keyword research and tracking",
            "Competitor analysis",
            "Technical SEO audits",
            "Content optimization suggestions",
            "Backlink analysis",
            "SERP tracking"
        ],
        "pricing_model": "Freemium",
        "pricing_details": "Free tier: 10 queries/day, Pro: $29/month, Enterprise: $99/month",
        "affiliate_url": "https://seo-master-pro.com/affiliate/join",
        "official_url": "https://seo-master-pro.com",
        "logo_url": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=200&h=200&fit=crop",
        "rating": 4.8,
        "total_reviews": 1247,
        "is_sponsored": True,
        "is_featured": True
    },
    {
        "id": "2",
        "name": "Content AI Generator",
        "description": "AI-powered content creation MCP server for marketing copy, blogs, and social media",
        "detailed_description": "Content AI Generator leverages advanced AI models to create high-quality marketing content, blog posts, social media captions, and ad copy. It understands your brand voice and optimizes content for SEO and engagement.",
        "category": "Content Generation",
        "features": [
            "AI-powered content creation",
            "SEO-optimized writing",
            "Multi-platform content adaptation",
            "Brand voice customization",
            "Content calendar integration",
            "Plagiarism detection",
            "Performance analytics"
        ],
        "pricing_model": "Paid",
        "pricing_details": "Starter: $19/month, Pro: $49/month, Agency: $149/month",
        "affiliate_url": "https://content-ai-gen.com/partners",
        "official_url": "https://content-ai-gen.com",
        "logo_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=200&h=200&fit=crop",
        "rating": 4.6,
        "total_reviews": 892,
        "is_sponsored": False,
        "is_featured": True
    },
    {
        "id": "3",
        "name": "Social Media Automation Hub",
        "description": "Complete social media management and automation MCP server for all platforms",
        "detailed_description": "Social Media Automation Hub provides comprehensive social media management across all major platforms. Schedule posts, analyze performance, engage with audiences, and automate repetitive tasks while maintaining authentic brand presence.",
        "category": "Social Media Management",
        "features": [
            "Multi-platform scheduling",
            "Automated engagement",
            "Performance analytics",
            "Content curation",
            "Hashtag optimization",
            "Competitor monitoring",
            "Influencer discovery"
        ],
        "pricing_model": "Freemium",
        "pricing_details": "Free: 3 accounts, Pro: $25/month, Business: $65/month",
        "affiliate_url": "https://social-hub-auto.com/affiliate",
        "official_url": "https://social-hub-auto.com",
        "logo_url": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=200&h=200&fit=crop",
        "rating": 4.4,
        "total_reviews": 654,
        "is_sponsored": True,
        "is_featured": True
    },
    {
        "id": "4",
        "name": "Email Marketing Maestro",
        "description": "Advanced email marketing automation and analytics MCP server",
        "detailed_description": "Email Marketing Maestro offers sophisticated email marketing automation, segmentation, and analytics. Create personalized campaigns, track performance, and optimize for maximum engagement and conversions.",
        "category": "Email Marketing",
        "features": [
            "Advanced segmentation",
            "A/B testing automation",
            "Personalization engine",
            "Behavioral triggers",
            "Analytics dashboard",
            "Deliverability optimization",
            "Integration hub"
        ],
        "pricing_model": "Paid",
        "pricing_details": "Growth: $39/month, Pro: $79/month, Enterprise: $199/month",
        "affiliate_url": "https://email-maestro.com/partners",
        "official_url": "https://email-maestro.com",
        "logo_url": "https://images.unsplash.com/photo-1596526131083-e8c633c948d2?w=200&h=200&fit=crop",
        "rating": 4.7,
        "total_reviews": 1053,
        "is_sponsored": False,
        "is_featured": True
    },
    {
        "id": "5",
        "name": "Performance Tracker Pro",
        "description": "Comprehensive marketing performance tracking and ROI analysis MCP server",
        "detailed_description": "Performance Tracker Pro provides unified marketing analytics across all channels. Track ROI, measure campaign performance, and get actionable insights to optimize your marketing spend and strategy.",
        "category": "Performance Tracking",
        "features": [
            "Multi-channel attribution",
            "ROI calculation",
            "Custom dashboard creation",
            "Automated reporting",
            "Goal tracking",
            "Data visualization",
            "Predictive analytics"
        ],
        "pricing_model": "Enterprise",
        "pricing_details": "Contact for pricing - starts at $299/month",
        "affiliate_url": "https://performance-tracker.com/referral",
        "official_url": "https://performance-tracker.com",
        "logo_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=200&h=200&fit=crop",
        "rating": 4.9,
        "total_reviews": 437,
        "is_sponsored": False,
        "is_featured": True
    },
    {
        "id": "6",
        "name": "Keyword Research Genius",
        "description": "Advanced keyword research and SEO optimization MCP server",
        "detailed_description": "Keyword Research Genius provides comprehensive keyword research, analysis, and optimization recommendations. Discover profitable keywords, analyze search intent, and optimize your content strategy for maximum visibility.",
        "category": "Keyword Research",
        "features": [
            "Keyword discovery",
            "Search intent analysis",
            "Difficulty scoring",
            "Competitor keyword gaps",
            "Content optimization",
            "Trend analysis",
            "Local SEO keywords"
        ],
        "pricing_model": "Freemium",
        "pricing_details": "Free: 5 searches/day, Pro: $35/month, Agency: $89/month",
        "affiliate_url": "https://keyword-genius.com/affiliate",
        "official_url": "https://keyword-genius.com",
        "logo_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=200&h=200&fit=crop",
        "rating": 4.5,
        "total_reviews": 789,
        "is_sponsored": True,
        "is_featured": False
    },
    {
        "id": "7",
        "name": "Competitor Intelligence AI",
        "description": "AI-powered competitor analysis and market intelligence MCP server",
        "detailed_description": "Competitor Intelligence AI monitors your competitors' digital strategies, tracks their content, analyzes their SEO performance, and provides actionable insights to stay ahead in your market.",
        "category": "Competitor Analysis",
        "features": [
            "Competitor monitoring",
            "Content analysis",
            "SEO gap analysis",
            "Pricing intelligence",
            "Ad campaign tracking",
            "Market share analysis",
            "Opportunity identification"
        ],
        "pricing_model": "Paid",
        "pricing_details": "Professional: $59/month, Business: $129/month, Enterprise: $299/month",
        "affiliate_url": "https://competitor-ai.com/partners",
        "official_url": "https://competitor-ai.com",
        "logo_url": "https://images.unsplash.com/photo-1551434678-e076c223a692?w=200&h=200&fit=crop",
        "rating": 4.3,
        "total_reviews": 523,
        "is_sponsored": False,
        "is_featured": False
    },
    {
        "id": "8",
        "name": "Marketing Automation Suite",
        "description": "Complete marketing automation and workflow management MCP server",
        "detailed_description": "Marketing Automation Suite provides end-to-end marketing automation capabilities. Create complex workflows, automate lead nurturing, manage customer journeys, and integrate with your existing marketing stack.",
        "category": "Marketing Automation",
        "features": [
            "Workflow automation",
            "Lead scoring",
            "Customer journey mapping",
            "Multi-channel campaigns",
            "Integration hub",
            "Advanced analytics",
            "Personalization engine"
        ],
        "pricing_model": "Enterprise",
        "pricing_details": "Starter: $99/month, Professional: $199/month, Enterprise: Custom",
        "affiliate_url": "https://marketing-automation.com/referral",
        "official_url": "https://marketing-automation.com",
        "logo_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=200&h=200&fit=crop",
        "rating": 4.6,
        "total_reviews": 672,
        "is_sponsored": False,
        "is_featured": True
    }
]

async def seed_database():
    """Seed the database with sample MCP servers"""
    
    # Clear existing data
    await db.mcp_servers.delete_many({})
    
    # Insert sample data
    await db.mcp_servers.insert_many(sample_servers)
    
    print(f"Successfully seeded {len(sample_servers)} MCP servers")

if __name__ == "__main__":
    asyncio.run(seed_database())