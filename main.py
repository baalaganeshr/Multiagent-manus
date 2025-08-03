#!/usr/bin/env python3
"""
Multiagent-manus: Indian Business Automation Platform
Main entry point that orchestrates all agents for Indian businesses.

Features:
- Website automation agents
- Marketing automation for Indian market
- Analytics and reporting
- WhatsApp Business integration
- UPI payment processing
- Multi-language support (Hindi/English)
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.env import settings
from agents.core_agents.orchestrator.master_orchestrator import MasterOrchestrator
from tools.whatsapp.whatsapp_integration import WhatsAppManager
from tools.payment.upi_gateway import UPIGateway

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('multiagent_manus.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class MultiagentManusApp:
    """Main application class for the Indian business automation platform."""
    
    def __init__(self):
        self.orchestrator = None
        self.whatsapp_manager = None
        self.upi_gateway = None
        self.is_running = False
    
    async def initialize(self):
        """Initialize all core components."""
        try:
            logger.info("Initializing Multiagent-manus for Indian business automation...")
            
            # Initialize core orchestrator
            self.orchestrator = MasterOrchestrator()
            await self.orchestrator.initialize()
            
            # Initialize WhatsApp Business integration
            if settings.WHATSAPP_ENABLED:
                self.whatsapp_manager = WhatsAppManager()
                await self.whatsapp_manager.initialize()
                logger.info("WhatsApp Business API initialized")
            
            # Initialize UPI payment gateway
            if settings.UPI_ENABLED:
                self.upi_gateway = UPIGateway()
                await self.upi_gateway.initialize()
                logger.info("UPI payment gateway initialized")
            
            logger.info("All components initialized successfully!")
            
        except Exception as e:
            logger.error(f"Failed to initialize application: {e}")
            raise
    
    async def start(self):
        """Start the application and all agent services."""
        if self.is_running:
            logger.warning("Application is already running")
            return
        
        try:
            await self.initialize()
            self.is_running = True
            
            logger.info("Starting Multiagent-manus platform...")
            
            # Start the orchestrator
            orchestrator_task = asyncio.create_task(
                self.orchestrator.start()
            )
            
            # Start WhatsApp service if enabled
            whatsapp_task = None
            if self.whatsapp_manager:
                whatsapp_task = asyncio.create_task(
                    self.whatsapp_manager.start_service()
                )
            
            # Start UPI gateway service if enabled
            upi_task = None
            if self.upi_gateway:
                upi_task = asyncio.create_task(
                    self.upi_gateway.start_service()
                )
            
            # Wait for all services
            tasks = [orchestrator_task]
            if whatsapp_task:
                tasks.append(whatsapp_task)
            if upi_task:
                tasks.append(upi_task)
            
            await asyncio.gather(*tasks)
            
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
            await self.shutdown()
        except Exception as e:
            logger.error(f"Application error: {e}")
            await self.shutdown()
            raise
    
    async def shutdown(self):
        """Gracefully shutdown all services."""
        if not self.is_running:
            return
        
        logger.info("Shutting down Multiagent-manus platform...")
        
        try:
            # Shutdown all components
            if self.orchestrator:
                await self.orchestrator.shutdown()
            
            if self.whatsapp_manager:
                await self.whatsapp_manager.shutdown()
            
            if self.upi_gateway:
                await self.upi_gateway.shutdown()
            
            self.is_running = False
            logger.info("Platform shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

async def main():
    """Main entry point for the application."""
    app = MultiagentManusApp()
    
    try:
        await app.start()
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Print banner
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║             Multiagent-manus Platform                    ║
    ║        Indian Business Automation Solution               ║
    ║                                                          ║
    ║  Features:                                               ║
    ║  • WhatsApp Business Integration                         ║
    ║  • UPI Payment Processing                                ║
    ║  • Multi-language Support (Hindi/English)               ║
    ║  • Website & Marketing Automation                        ║
    ║  • Analytics & Reporting                                 ║
    ║  • GST Compliance & Festival Marketing                   ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGracefully shutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
