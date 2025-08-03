"""
Master Orchestrator for Multiagent-manus Platform
Coordinates all agents for Indian business automation.

This orchestrator manages:
- Website agents (content, SEO, builder)
- Marketing agents (campaigns, social media, local marketing)
- Analytics agents (data collection, insights, reporting)
- Core communication and quality control
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from config.env import settings
from agents.website_agents.website_builder.builder_agent import WebsiteBuilderAgent
from agents.website_agents.content_manager.content_agent import ContentManagerAgent
from agents.website_agents.seo_optimizer.seo_agent import SEOOptimizerAgent

from agents.marketing_agents.campaign_manager.campaign_agent import CampaignManagerAgent
from agents.marketing_agents.social_media.social_agent import SocialMediaAgent
from agents.marketing_agents.local_marketing.local_agent import LocalMarketingAgent

from agents.analytics_agents.data_collector.collector_agent import DataCollectorAgent
from agents.analytics_agents.insights_engine.insights_agent import InsightsEngineAgent
from agents.analytics_agents.report_generator.report_agent import ReportGeneratorAgent

from agents.core_agents.customer_communication.communication_agent import CustomerCommunicationAgent
from agents.core_agents.quality_control.quality_agent import QualityControlAgent

logger = logging.getLogger(__name__)

class MasterOrchestrator:
    """
    Main orchestrator that coordinates all agents for Indian business automation.
    Handles request routing, agent communication, and business workflow management.
    """
    
    def __init__(self):
        self.agents = {}
        self.is_initialized = False
        self.is_running = False
        self.task_queue = asyncio.Queue()
        self.active_tasks = {}
        
        # Indian business context
        self.business_context = {
            "languages": ["hi", "en"],  # Hindi and English
            "currencies": ["INR"],
            "payment_methods": ["UPI", "Net Banking", "Cards", "Wallet"],
            "festivals": self._load_indian_festivals(),
            "business_hours": {
                "start": "09:00",
                "end": "18:00",
                "timezone": "Asia/Kolkata"
            }
        }
    
    async def initialize(self):
        """Initialize all agents and core systems."""
        if self.is_initialized:
            logger.warning("Orchestrator already initialized")
            return
        
        logger.info("Initializing Master Orchestrator...")
        
        try:
            # Initialize Website Agents
            self.agents["website_builder"] = WebsiteBuilderAgent()
            self.agents["content_manager"] = ContentManagerAgent()
            self.agents["seo_optimizer"] = SEOOptimizerAgent()
            
            # Initialize Marketing Agents
            self.agents["campaign_manager"] = CampaignManagerAgent()
            self.agents["social_media"] = SocialMediaAgent()
            self.agents["local_marketing"] = LocalMarketingAgent()
            
            # Initialize Analytics Agents
            self.agents["data_collector"] = DataCollectorAgent()
            self.agents["insights_engine"] = InsightsEngineAgent()
            self.agents["report_generator"] = ReportGeneratorAgent()
            
            # Initialize Core Agents
            self.agents["customer_communication"] = CustomerCommunicationAgent()
            self.agents["quality_control"] = QualityControlAgent()
            
            # Initialize all agents
            for agent_name, agent in self.agents.items():
                await agent.initialize()
                logger.info(f"Initialized {agent_name} agent")
            
            self.is_initialized = True
            logger.info("Master Orchestrator initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize orchestrator: {e}")
            raise
    
    async def start(self):
        """Start the orchestrator and begin processing requests."""
        if not self.is_initialized:
            await self.initialize()
        
        if self.is_running:
            logger.warning("Orchestrator is already running")
            return
        
        self.is_running = True
        logger.info("Starting Master Orchestrator...")
        
        # Start task processing
        task_processor = asyncio.create_task(self._process_tasks())
        
        try:
            await task_processor
        except Exception as e:
            logger.error(f"Error in orchestrator: {e}")
            raise
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a business automation request.
        
        Args:
            request: Dictionary containing request details
                - type: Request type (website, marketing, analytics)
                - action: Specific action to perform
                - data: Request data
                - customer_id: Customer identifier
                - language: Preferred language (hi/en)
        
        Returns:
            Response dictionary with results
        """
        request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"Processing request {request_id}: {request.get('type', 'unknown')}")
        
        try:
            # Validate request
            if not self._validate_request(request):
                return {
                    "status": "error",
                    "message": "Invalid request format",
                    "request_id": request_id
                }
            
            # Route request to appropriate agents
            response = await self._route_request(request_id, request)
            
            # Quality check
            if settings.QUALITY_CHECK_ENABLED:
                response = await self.agents["quality_control"].review_response(response)
            
            logger.info(f"Request {request_id} processed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error processing request {request_id}: {e}")
            return {
                "status": "error",
                "message": f"Processing failed: {str(e)}",
                "request_id": request_id
            }
    
    async def _route_request(self, request_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Route request to appropriate agents based on type."""
        request_type = request.get("type", "").lower()
        action = request.get("action", "")
        
        if request_type == "website":
            return await self._handle_website_request(request_id, request)
        elif request_type == "marketing":
            return await self._handle_marketing_request(request_id, request)
        elif request_type == "analytics":
            return await self._handle_analytics_request(request_id, request)
        elif request_type == "communication":
            return await self._handle_communication_request(request_id, request)
        else:
            # Default to customer communication for general queries
            return await self.agents["customer_communication"].handle_request(request)
    
    async def _handle_website_request(self, request_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle website-related requests."""
        action = request.get("action", "").lower()
        
        if action in ["build", "create", "develop"]:
            return await self.agents["website_builder"].handle_request(request)
        elif action in ["content", "update", "modify"]:
            return await self.agents["content_manager"].handle_request(request)
        elif action in ["seo", "optimize", "ranking"]:
            return await self.agents["seo_optimizer"].handle_request(request)
        else:
            # Coordinate multiple website agents for complex requests
            return await self._coordinate_website_agents(request)
    
    async def _handle_marketing_request(self, request_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle marketing-related requests."""
        action = request.get("action", "").lower()
        
        if action in ["campaign", "advertise", "promote"]:
            return await self.agents["campaign_manager"].handle_request(request)
        elif action in ["social", "instagram", "facebook", "twitter"]:
            return await self.agents["social_media"].handle_request(request)
        elif action in ["local", "regional", "community"]:
            return await self.agents["local_marketing"].handle_request(request)
        else:
            # Coordinate multiple marketing agents
            return await self._coordinate_marketing_agents(request)
    
    async def _handle_analytics_request(self, request_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle analytics-related requests."""
        action = request.get("action", "").lower()
        
        if action in ["collect", "gather", "data"]:
            return await self.agents["data_collector"].handle_request(request)
        elif action in ["analyze", "insights", "trends"]:
            return await self.agents["insights_engine"].handle_request(request)
        elif action in ["report", "summary", "dashboard"]:
            return await self.agents["report_generator"].handle_request(request)
        else:
            # Coordinate analytics pipeline
            return await self._coordinate_analytics_agents(request)
    
    async def _handle_communication_request(self, request_id: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer communication requests."""
        return await self.agents["customer_communication"].handle_request(request)
    
    async def _coordinate_website_agents(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate multiple website agents for complex requests."""
        results = {}
        
        # Build website structure
        build_result = await self.agents["website_builder"].handle_request(request)
        results["build"] = build_result
        
        # Generate and manage content
        content_result = await self.agents["content_manager"].handle_request(request)
        results["content"] = content_result
        
        # Optimize for SEO
        seo_result = await self.agents["seo_optimizer"].handle_request(request)
        results["seo"] = seo_result
        
        return {
            "status": "success",
            "message": "Website agents coordinated successfully",
            "results": results
        }
    
    async def _coordinate_marketing_agents(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate multiple marketing agents for comprehensive campaigns."""
        results = {}
        
        # Create marketing campaign
        campaign_result = await self.agents["campaign_manager"].handle_request(request)
        results["campaign"] = campaign_result
        
        # Social media promotion
        social_result = await self.agents["social_media"].handle_request(request)
        results["social"] = social_result
        
        # Local marketing initiatives
        local_result = await self.agents["local_marketing"].handle_request(request)
        results["local"] = local_result
        
        return {
            "status": "success",
            "message": "Marketing agents coordinated successfully",
            "results": results
        }
    
    async def _coordinate_analytics_agents(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate analytics pipeline for comprehensive insights."""
        # Data collection
        collect_result = await self.agents["data_collector"].handle_request(request)
        
        # Generate insights from collected data
        insights_request = {**request, "data": collect_result.get("data", {})}
        insights_result = await self.agents["insights_engine"].handle_request(insights_request)
        
        # Generate reports
        report_request = {**request, "insights": insights_result.get("insights", {})}
        report_result = await self.agents["report_generator"].handle_request(report_request)
        
        return {
            "status": "success",
            "message": "Analytics pipeline completed successfully",
            "results": {
                "data_collection": collect_result,
                "insights": insights_result,
                "report": report_result
            }
        }
    
    async def _process_tasks(self):
        """Process queued tasks asynchronously."""
        while self.is_running:
            try:
                # Wait for task with timeout
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                
                # Process task
                task_id = task.get("id")
                self.active_tasks[task_id] = task
                
                # Execute task
                result = await self.process_request(task.get("request", {}))
                
                # Store result
                task["result"] = result
                task["completed_at"] = datetime.now()
                
                # Remove from active tasks
                del self.active_tasks[task_id]
                
                # Mark task as done
                self.task_queue.task_done()
                
            except asyncio.TimeoutError:
                # No tasks in queue, continue
                continue
            except Exception as e:
                logger.error(f"Error processing task: {e}")
    
    def _validate_request(self, request: Dict[str, Any]) -> bool:
        """Validate request format and required fields."""
        required_fields = ["type"]
        return all(field in request for field in required_fields)
    
    def _load_indian_festivals(self) -> List[Dict[str, Any]]:
        """Load Indian festival calendar for marketing timing."""
        return [
            {"name": "Diwali", "date": "2024-11-01", "type": "major"},
            {"name": "Holi", "date": "2024-03-08", "type": "major"},
            {"name": "Dussehra", "date": "2024-10-12", "type": "major"},
            {"name": "Eid ul-Fitr", "date": "2024-04-10", "type": "major"},
            {"name": "Christmas", "date": "2024-12-25", "type": "major"},
            {"name": "Karva Chauth", "date": "2024-11-01", "type": "regional"},
            {"name": "Raksha Bandhan", "date": "2024-08-19", "type": "regional"},
            {"name": "Ganesh Chaturthi", "date": "2024-09-07", "type": "regional"}
        ]
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        status = {}
        for agent_name, agent in self.agents.items():
            try:
                agent_status = await agent.get_status()
                status[agent_name] = agent_status
            except Exception as e:
                status[agent_name] = {"status": "error", "error": str(e)}
        
        return {
            "orchestrator_status": "running" if self.is_running else "stopped",
            "agents": status,
            "active_tasks": len(self.active_tasks),
            "queue_size": self.task_queue.qsize()
        }
    
    async def shutdown(self):
        """Gracefully shutdown the orchestrator and all agents."""
        logger.info("Shutting down Master Orchestrator...")
        
        self.is_running = False
        
        # Shutdown all agents
        for agent_name, agent in self.agents.items():
            try:
                await agent.shutdown()
                logger.info(f"Shutdown {agent_name} agent")
            except Exception as e:
                logger.error(f"Error shutting down {agent_name}: {e}")
        
        # Wait for remaining tasks
        if not self.task_queue.empty():
            logger.info("Waiting for remaining tasks to complete...")
            await self.task_queue.join()
        
        logger.info("Master Orchestrator shutdown complete")
