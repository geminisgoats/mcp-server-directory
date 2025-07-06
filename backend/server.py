from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
from enum import Enum

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="MCP Server Directory API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Enums for better data structure
class MCPCategory(str, Enum):
    SEO_ANALYTICS = "SEO Analytics"
    CONTENT_GENERATION = "Content Generation"
    SOCIAL_MEDIA = "Social Media Management"
    EMAIL_MARKETING = "Email Marketing"
    PERFORMANCE_TRACKING = "Performance Tracking"
    KEYWORD_RESEARCH = "Keyword Research"
    COMPETITOR_ANALYSIS = "Competitor Analysis"
    AUTOMATION = "Marketing Automation"

class PricingModel(str, Enum):
    FREE = "Free"
    FREEMIUM = "Freemium"
    PAID = "Paid"
    ENTERPRISE = "Enterprise"

# Data Models
class MCPServer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    detailed_description: str
    category: MCPCategory
    features: List[str]
    pricing_model: PricingModel
    pricing_details: str
    affiliate_url: str
    official_url: str
    logo_url: str
    rating: float = Field(ge=0, le=5)
    total_reviews: int = Field(default=0)
    is_sponsored: bool = Field(default=False)
    is_featured: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MCPServerCreate(BaseModel):
    name: str
    description: str
    detailed_description: str
    category: MCPCategory
    features: List[str]
    pricing_model: PricingModel
    pricing_details: str
    affiliate_url: str
    official_url: str
    logo_url: str
    rating: float = Field(ge=0, le=5)
    total_reviews: int = Field(default=0)
    is_sponsored: bool = Field(default=False)
    is_featured: bool = Field(default=False)

class ClickTracking(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    server_id: str
    user_ip: str
    user_agent: str
    referrer: Optional[str] = None
    click_type: str  # "affiliate", "official", "details"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ClickTrackingCreate(BaseModel):
    server_id: str
    user_ip: str
    user_agent: str
    referrer: Optional[str] = None
    click_type: str

# API Endpoints
@api_router.get("/")
async def root():
    return {"message": "MCP Server Directory API", "version": "1.0.0"}

@api_router.get("/servers", response_model=List[MCPServer])
async def get_servers(
    category: Optional[MCPCategory] = None,
    pricing_model: Optional[PricingModel] = None,
    search: Optional[str] = None,
    featured_only: bool = False,
    limit: int = Query(default=50, le=100)
):
    """Get MCP servers with optional filtering"""
    query = {}
    
    if category:
        query["category"] = category
    
    if pricing_model:
        query["pricing_model"] = pricing_model
    
    if featured_only:
        query["is_featured"] = True
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"features": {"$regex": search, "$options": "i"}}
        ]
    
    servers = await db.mcp_servers.find(query).sort([("is_sponsored", -1), ("is_featured", -1), ("rating", -1)]).limit(limit).to_list(limit)
    return [MCPServer(**server) for server in servers]

@api_router.get("/servers/{server_id}", response_model=MCPServer)
async def get_server(server_id: str):
    """Get a specific MCP server by ID"""
    server = await db.mcp_servers.find_one({"id": server_id})
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return MCPServer(**server)

@api_router.post("/servers", response_model=MCPServer)
async def create_server(server: MCPServerCreate):
    """Create a new MCP server listing"""
    server_dict = server.dict()
    server_obj = MCPServer(**server_dict)
    await db.mcp_servers.insert_one(server_obj.dict())
    return server_obj

@api_router.put("/servers/{server_id}", response_model=MCPServer)
async def update_server(server_id: str, server: MCPServerCreate):
    """Update an existing MCP server"""
    server_dict = server.dict()
    server_dict["updated_at"] = datetime.utcnow()
    
    result = await db.mcp_servers.update_one(
        {"id": server_id},
        {"$set": server_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Server not found")
    
    updated_server = await db.mcp_servers.find_one({"id": server_id})
    return MCPServer(**updated_server)

@api_router.delete("/servers/{server_id}")
async def delete_server(server_id: str):
    """Delete a MCP server"""
    result = await db.mcp_servers.delete_one({"id": server_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Server not found")
    return {"message": "Server deleted successfully"}

@api_router.get("/categories")
async def get_categories():
    """Get all available categories"""
    return [{"value": cat.value, "label": cat.value} for cat in MCPCategory]

@api_router.get("/featured-servers", response_model=List[MCPServer])
async def get_featured_servers(limit: int = Query(default=6, le=20)):
    """Get featured MCP servers for homepage"""
    servers = await db.mcp_servers.find({"is_featured": True}).sort([("rating", -1)]).limit(limit).to_list(limit)
    return [MCPServer(**server) for server in servers]

@api_router.get("/sponsored-servers", response_model=List[MCPServer])
async def get_sponsored_servers(limit: int = Query(default=3, le=10)):
    """Get sponsored MCP servers"""
    servers = await db.mcp_servers.find({"is_sponsored": True}).sort([("rating", -1)]).limit(limit).to_list(limit)
    return [MCPServer(**server) for server in servers]

@api_router.post("/track-click", response_model=ClickTracking)
async def track_click(click: ClickTrackingCreate):
    """Track affiliate and other clicks for analytics"""
    click_dict = click.dict()
    click_obj = ClickTracking(**click_dict)
    await db.click_tracking.insert_one(click_obj.dict())
    return click_obj

@api_router.get("/stats/{server_id}")
async def get_server_stats(server_id: str):
    """Get click statistics for a server"""
    total_clicks = await db.click_tracking.count_documents({"server_id": server_id})
    affiliate_clicks = await db.click_tracking.count_documents({"server_id": server_id, "click_type": "affiliate"})
    
    return {
        "server_id": server_id,
        "total_clicks": total_clicks,
        "affiliate_clicks": affiliate_clicks,
        "conversion_rate": (affiliate_clicks / total_clicks * 100) if total_clicks > 0 else 0
    }

@api_router.get("/analytics")
async def get_analytics():
    """Get overall platform analytics"""
    total_servers = await db.mcp_servers.count_documents({})
    total_clicks = await db.click_tracking.count_documents({})
    featured_servers = await db.mcp_servers.count_documents({"is_featured": True})
    sponsored_servers = await db.mcp_servers.count_documents({"is_sponsored": True})
    
    return {
        "total_servers": total_servers,
        "total_clicks": total_clicks,
        "featured_servers": featured_servers,
        "sponsored_servers": sponsored_servers
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()