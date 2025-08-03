"""
Website Builder Agent for Indian Businesses
Creates responsive, SEO-optimized websites with Hindi/English support.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class WebsiteBuilderAgent:
    """Website Builder Agent for creating Indian business websites."""
    
    def __init__(self):
        self.agent_name = "website_builder"
        self.is_initialized = False
        
        # Indian business website templates
        self.templates = {
            "restaurant": {
                "name": "Restaurant & Cafe Template",
                "features": ["menu_display", "online_ordering", "table_booking", "reviews"],
                "languages": ["hi", "en"],
                "payment_integration": True,
                "whatsapp_integration": True
            },
            "retail": {
                "name": "Retail Store Template", 
                "features": ["product_catalog", "inventory_management", "customer_accounts", "loyalty_program"],
                "languages": ["hi", "en"],
                "payment_integration": True,
                "whatsapp_integration": True
            },
            "service": {
                "name": "Service Provider Template",
                "features": ["service_listing", "appointment_booking", "testimonials", "contact_forms"],
                "languages": ["hi", "en"],
                "payment_integration": True,
                "whatsapp_integration": True
            },
            "ecommerce": {
                "name": "E-commerce Store Template",
                "features": ["product_catalog", "shopping_cart", "payment_gateway", "order_tracking"],
                "languages": ["hi", "en"],
                "payment_integration": True,
                "whatsapp_integration": True
            }
        }
    
    async def initialize(self):
        """Initialize the website builder agent."""
        self.is_initialized = True
        logger.info("Website Builder Agent initialized")
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle website building requests."""
        try:
            business_type = self._detect_business_type(request)
            website_config = await self._create_website_config(business_type, request)
            
            return {
                "status": "success",
                "agent": self.agent_name,
                "business_type": business_type,
                "website_config": website_config,
                "estimated_time": "3-5 business days",
                "next_steps": [
                    "Domain registration and hosting setup",
                    "Content creation in Hindi and English", 
                    "Payment gateway integration",
                    "WhatsApp Business integration",
                    "SEO optimization"
                ]
            }
            
        except Exception as e:
            logger.error(f"Website builder error: {e}")
            return {
                "status": "error",
                "agent": self.agent_name,
                "error": str(e)
            }
    
    def _detect_business_type(self, request: Dict[str, Any]) -> str:
        """Detect business type from request."""
        description = request.get("description", "").lower()
        business_data = request.get("business_data", {})
        
        if any(word in description for word in ["restaurant", "cafe", "food", "खाना", "रेस्टोरेंट"]):
            return "restaurant"
        elif any(word in description for word in ["shop", "store", "retail", "दुकान", "स्टोर"]):
            return "retail"
        elif any(word in description for word in ["service", "consulting", "सेवा", "सलाह"]):
            return "service"
        elif any(word in description for word in ["ecommerce", "online", "ऑनलाइन"]):
            return "ecommerce"
        else:
            return "service"  # Default
    
    async def _create_website_config(self, business_type: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Create website configuration based on business type."""
        template = self.templates.get(business_type, self.templates["service"])
        
        config = {
            "template": template,
            "domain_suggestions": self._generate_domain_suggestions(request),
            "pages": self._get_recommended_pages(business_type),
            "features": template["features"],
            "seo_keywords": self._generate_seo_keywords(business_type, request),
            "payment_methods": ["UPI", "Net Banking", "Cards", "Wallets"],
            "languages": ["hi", "en"],
            "responsive_design": True,
            "mobile_optimized": True
        }
        
        return config
    
    def _generate_domain_suggestions(self, request: Dict[str, Any]) -> List[str]:
        """Generate domain name suggestions."""
        business_name = request.get("business_data", {}).get("name", "business")
        clean_name = business_name.lower().replace(" ", "")
        
        return [
            f"{clean_name}.in",
            f"{clean_name}.co.in", 
            f"{clean_name}online.in",
            f"{clean_name}india.com",
            f"my{clean_name}.in"
        ]
    
    def _get_recommended_pages(self, business_type: str) -> List[str]:
        """Get recommended pages for business type."""
        common_pages = ["home", "about", "contact", "privacy"]
        
        business_pages = {
            "restaurant": ["menu", "gallery", "reservations", "reviews"],
            "retail": ["products", "categories", "cart", "account"], 
            "service": ["services", "portfolio", "testimonials", "booking"],
            "ecommerce": ["shop", "categories", "cart", "checkout", "account"]
        }
        
        return common_pages + business_pages.get(business_type, [])
    
    def _generate_seo_keywords(self, business_type: str, request: Dict[str, Any]) -> List[str]:
        """Generate SEO keywords for Indian market."""
        location = request.get("business_data", {}).get("location", "India")
        business_name = request.get("business_data", {}).get("name", "")
        
        base_keywords = {
            "restaurant": [
                f"restaurant in {location}",
                f"food delivery {location}",
                f"best restaurant {location}",
                f"{location} restaurant",
                "online food ordering",
                "table booking"
            ],
            "retail": [
                f"shop in {location}",
                f"store {location}",
                f"online shopping {location}",
                f"buy online {location}",
                "retail store",
                "online store"
            ],
            "service": [
                f"services in {location}",
                f"service provider {location}",
                f"best services {location}",
                "professional services",
                "consultation services"
            ]
        }
        
        keywords = base_keywords.get(business_type, base_keywords["service"])
        if business_name:
            keywords.extend([business_name, f"{business_name} {location}"])
        
        return keywords
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent": self.agent_name,
            "status": "active" if self.is_initialized else "inactive",
            "templates_available": len(self.templates),
            "features": ["responsive_design", "seo_optimization", "multi_language", "payment_integration"]
        }
    
    async def shutdown(self):
        """Shutdown the agent."""
        self.is_initialized = False
        logger.info("Website Builder Agent shutdown")
