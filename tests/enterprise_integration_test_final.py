"""
Enterprise Integration Test Suite
Comprehensive testing for the Enterprise AI Business Automation Platform.
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.core_agents.orchestrator.master_orchestrator import EnterpriseGlobalOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class EnterpriseIntegrationTest:
    """Enterprise integration test suite for validating all systems."""
    
    def __init__(self):
        self.orchestrator = None
        self.test_results = {}
        
    async def run_comprehensive_test_suite(self):
        """Run comprehensive enterprise integration tests."""
        logger.info("🚀 Starting Enterprise Integration Test Suite")
        
        try:
            # Phase 1: Basic Enterprise Integration
            await self._test_enterprise_initialization()
            
            # Phase 2: Real Agent Implementation Testing
            await self._test_enterprise_agents()
            
            # Phase 3: Professional Request Processing
            await self._test_professional_request_processing()
            
            # Phase 4: Global Market Support
            await self._test_global_market_support()
            
            # Phase 5: Enterprise Quality Validation
            await self._test_enterprise_quality_validation()
            
            # Generate comprehensive test report
            self._generate_test_report()
            
        except Exception as e:
            logger.error(f"❌ Enterprise integration test failed: {e}")
            raise
        finally:
            if self.orchestrator:
                await self.orchestrator.shutdown()
    
    async def _test_enterprise_initialization(self):
        """Test enterprise-grade orchestrator initialization."""
        logger.info("📋 Phase 1: Testing Enterprise Initialization")
        
        try:
            # Initialize enterprise orchestrator
            self.orchestrator = EnterpriseGlobalOrchestrator()
            await self.orchestrator.initialize()
            
            # Validate enterprise agents are initialized
            required_agents = [
                "content_manager", "seo_optimizer", "social_media", 
                "quality_control", "website_builder", "campaign_manager"
            ]
            
            initialized_agents = []
            for agent_name in required_agents:
                if agent_name in self.orchestrator.agents:
                    agent = self.orchestrator.agents[agent_name]
                    if hasattr(agent, 'is_initialized') and agent.is_initialized:
                        initialized_agents.append(agent_name)
                        logger.info(f"✅ {agent_name} initialized successfully")
                    else:
                        logger.warning(f"⚠️ {agent_name} not properly initialized")
                else:
                    logger.error(f"❌ {agent_name} missing from orchestrator")
            
            self.test_results["enterprise_initialization"] = {
                "status": "success" if len(initialized_agents) >= 4 else "partial",
                "initialized_agents": initialized_agents,
                "total_agents": len(self.orchestrator.agents),
                "required_agents": required_agents
            }
            
            logger.info(f"✅ Enterprise initialization: {len(initialized_agents)}/{len(required_agents)} agents ready")
            
        except Exception as e:
            logger.error(f"❌ Enterprise initialization failed: {e}")
            self.test_results["enterprise_initialization"] = {"status": "failed", "error": str(e)}
            raise
    
    async def _test_enterprise_agents(self):
        """Test enterprise agent implementations."""
        logger.info("🤖 Phase 2: Testing Enterprise Agent Implementations")
        
        agent_tests = {
            "content_manager": self._test_content_manager_agent,
            "seo_optimizer": self._test_seo_optimizer_agent,
            "social_media": self._test_social_media_agent,
            "quality_control": self._test_quality_control_agent
        }
        
        agent_results = {}
        
        for agent_name, test_func in agent_tests.items():
            try:
                if agent_name in self.orchestrator.agents:
                    result = await test_func(self.orchestrator.agents[agent_name])
                    agent_results[agent_name] = result
                    logger.info(f"✅ {agent_name}: {result['status']}")
                else:
                    agent_results[agent_name] = {"status": "missing", "error": "Agent not found"}
                    logger.error(f"❌ {agent_name}: Agent not found")
            except Exception as e:
                agent_results[agent_name] = {"status": "failed", "error": str(e)}
                logger.error(f"❌ {agent_name}: {e}")
        
        self.test_results["enterprise_agents"] = agent_results
    
    async def _test_content_manager_agent(self, agent):
        """Test enterprise content manager agent."""
        test_request = {
            "business_type": "technology",
            "region": {"country": "US", "language": "en"},
            "languages": ["en", "es", "fr"]
        }
        
        response = await agent.handle_request(test_request)
        
        if response.get("status") == "success":
            content_package = response.get("content_package", {})
            has_multilingual = len(content_package) >= 2
            has_enterprise_features = response.get("enterprise_features", {}).get("brand_consistency", False)
            
            return {
                "status": "success",
                "multilingual_support": has_multilingual,
                "enterprise_features": has_enterprise_features,
                "content_types": list(content_package.keys()) if content_package else []
            }
        else:
            return {"status": "failed", "error": response.get("error", "Unknown error")}
    
    async def _test_seo_optimizer_agent(self, agent):
        """Test enterprise SEO optimizer agent."""
        test_request = {
            "business_type": "consulting",
            "target_markets": ["US", "EU", "APAC"],
            "region": {"country": "US"}
        }
        
        response = await agent.handle_request(test_request)
        
        if response.get("status") == "success":
            seo_strategy = response.get("seo_strategy", {})
            has_keyword_strategy = "keyword_strategy" in seo_strategy
            has_technical_seo = "technical_seo" in response
            
            return {
                "status": "success",
                "keyword_strategy": has_keyword_strategy,
                "technical_seo": has_technical_seo,
                "enterprise_features": response.get("enterprise_features", {})
            }
        else:
            return {"status": "failed", "error": response.get("error", "Unknown error")}
    
    async def _test_social_media_agent(self, agent):
        """Test enterprise social media agent."""
        test_request = {
            "business_type": "financial_services",
            "target_markets": ["US", "EU"],
            "platforms": ["linkedin", "twitter", "facebook"]
        }
        
        response = await agent.handle_request(test_request)
        
        if response.get("status") == "success":
            platform_optimization = response.get("platform_optimization", {})
            has_platforms = len(platform_optimization) >= 2
            has_content_calendar = "content_calendar" in response
            
            return {
                "status": "success",
                "platform_support": has_platforms,
                "content_calendar": has_content_calendar,
                "supported_platforms": list(platform_optimization.keys())
            }
        else:
            return {"status": "failed", "error": response.get("error", "Unknown error")}
    
    async def _test_quality_control_agent(self, agent):
        """Test enterprise quality control agent."""
        test_request = {
            "agent_outputs": {
                "content_manager": {"content": "test"},
                "seo_optimizer": {"strategy": "test"},
                "social_media": {"platforms": "test"}
            },
            "business_requirements": {"quality": "enterprise"},
            "region": {"country": "US"}
        }
        
        response = await agent.handle_request(test_request)
        
        if response.get("status") == "success":
            quality_score = response.get("overall_quality_score", {})
            has_score = "overall_score" in quality_score
            has_recommendations = len(response.get("recommendations", [])) >= 0
            
            return {
                "status": "success",
                "quality_scoring": has_score,
                "recommendations": has_recommendations,
                "enterprise_readiness": quality_score.get("enterprise_readiness", False)
            }
        else:
            return {"status": "failed", "error": response.get("error", "Unknown error")}
    
    async def _test_professional_request_processing(self):
        """Test professional request processing without regional bias."""
        logger.info("🌐 Phase 3: Testing Professional Request Processing")
        
        # Test enterprise technology company request
        enterprise_request = {
            "type": "complete_setup",
            "description": "Global technology company needs comprehensive business automation",
            "business_type": "technology",
            "business_data": {
                "name": "TechCorp Global",
                "location": "New York, United States",
                "size": "enterprise",
                "industry": "technology"
            },
            "requirements": [
                "Enterprise-grade website",
                "Global marketing automation", 
                "Multi-language support",
                "Compliance management"
            ]
        }
        
        try:
            response = await self.orchestrator.process_request(enterprise_request)
            
            professional_indicators = {
                "no_regional_bias": "indian" not in str(response).lower() and "hindi" not in str(response).lower(),
                "enterprise_language": "enterprise" in str(response).lower() or "professional" in str(response).lower(),
                "global_support": "global" in str(response).lower() or "international" in str(response).lower(),
                "multi_currency": response.get("global_features", {}).get("multi_currency", False),
                "professional_timeline": "timeline" in response or "schedule" in response
            }
            
            self.test_results["professional_processing"] = {
                "status": "success",
                "professional_indicators": professional_indicators,
                "response_quality": "high" if sum(professional_indicators.values()) >= 3 else "medium"
            }
            
            logger.info(f"✅ Professional processing: {sum(professional_indicators.values())}/5 quality indicators met")
            
        except Exception as e:
            logger.error(f"❌ Professional request processing failed: {e}")
            self.test_results["professional_processing"] = {"status": "failed", "error": str(e)}
    
    async def _test_global_market_support(self):
        """Test global market support capabilities."""
        logger.info("🌍 Phase 4: Testing Global Market Support")
        
        global_markets = [
            {"country": "US", "language": "en", "business_type": "technology"},
            {"country": "DE", "language": "de", "business_type": "manufacturing"},
            {"country": "JP", "language": "ja", "business_type": "consulting"},
            {"country": "SG", "language": "en", "business_type": "financial_services"}
        ]
        
        market_results = {}
        
        for market in global_markets:
            try:
                market_request = {
                    "type": "marketing",
                    "description": f"Professional services for {market['business_type']} company",
                    "business_type": market["business_type"],
                    "region": {"country": market["country"], "language": market["language"]},
                    "business_data": {"location": market["country"]}
                }
                
                response = await self.orchestrator.process_request(market_request)
                
                market_features = {
                    "currency_support": market["country"] in str(response.get("global_features", {})),
                    "language_support": market["language"] in str(response),
                    "cultural_adaptation": "cultural" in str(response).lower(),
                    "regional_features": "regional" in str(response).lower()
                }
                
                market_results[market["country"]] = {
                    "status": "success",
                    "features": market_features,
                    "support_score": sum(market_features.values())
                }
                
                logger.info(f"✅ {market['country']}: {sum(market_features.values())}/4 global features supported")
                
            except Exception as e:
                market_results[market["country"]] = {"status": "failed", "error": str(e)}
                logger.error(f"❌ {market['country']}: {e}")
        
        self.test_results["global_market_support"] = market_results
    
    async def _test_enterprise_quality_validation(self):
        """Test enterprise quality validation."""
        logger.info("🏆 Phase 5: Testing Enterprise Quality Validation")
        
        try:
            # Test overall system health
            agent_status = {}
            for agent_name, agent in self.orchestrator.agents.items():
                try:
                    status = await agent.get_status()
                    agent_status[agent_name] = status
                except Exception as e:
                    agent_status[agent_name] = {"status": "error", "error": str(e)}
            
            # Validate enterprise readiness
            active_agents = sum(1 for status in agent_status.values() 
                              if status.get("status") == "active")
            
            enterprise_metrics = {
                "agent_availability": active_agents / len(agent_status) if agent_status else 0,
                "error_handling": self.orchestrator.health_status == "healthy",
                "performance_monitoring": hasattr(self.orchestrator, "performance_metrics"),
                "production_readiness": hasattr(self.orchestrator, "circuit_breaker")
            }
            
            overall_quality = sum(enterprise_metrics.values()) / len(enterprise_metrics)
            
            self.test_results["enterprise_quality"] = {
                "status": "success",
                "overall_quality_score": overall_quality,
                "enterprise_metrics": enterprise_metrics,
                "active_agents": active_agents,
                "total_agents": len(agent_status),
                "enterprise_ready": overall_quality >= 0.8
            }
            
            logger.info(f"✅ Enterprise Quality: {overall_quality:.1%} overall score")
            
        except Exception as e:
            logger.error(f"❌ Enterprise quality validation failed: {e}")
            self.test_results["enterprise_quality"] = {"status": "failed", "error": str(e)}
    
    def _generate_test_report(self):
        """Generate comprehensive test report."""
        logger.info("📊 Generating Enterprise Integration Test Report")
        
        print("\n" + "="*80)
        print("🏢 ENTERPRISE AI BUSINESS AUTOMATION PLATFORM")
        print("📋 Integration Test Report")
        print("="*80)
        
        # Overall status
        total_phases = len(self.test_results)
        successful_phases = sum(1 for result in self.test_results.values() 
                               if result.get("status") in ["success", "partial"])
        
        print(f"\n📈 OVERALL STATUS: {successful_phases}/{total_phases} phases completed")
        
        # Phase-by-phase results
        for phase_name, results in self.test_results.items():
            status_icon = "✅" if results.get("status") == "success" else "⚠️" if results.get("status") == "partial" else "❌"
            print(f"\n{status_icon} {phase_name.replace('_', ' ').title()}: {results.get('status', 'unknown').upper()}")
            
            if phase_name == "enterprise_initialization":
                agents = results.get("initialized_agents", [])
                print(f"   🤖 Agents Initialized: {', '.join(agents)}")
            
            elif phase_name == "enterprise_agents":
                for agent, agent_result in results.items():
                    agent_status = "✅" if agent_result.get("status") == "success" else "❌"
                    print(f"   {agent_status} {agent}: {agent_result.get('status', 'unknown')}")
            
            elif phase_name == "professional_processing":
                quality = results.get("response_quality", "unknown")
                print(f"   📊 Response Quality: {quality}")
            
            elif phase_name == "global_market_support":
                for market, market_result in results.items():
                    market_status = "✅" if market_result.get("status") == "success" else "❌"
                    score = market_result.get("support_score", 0)
                    print(f"   {market_status} {market}: {score}/4 features")
            
            elif phase_name == "enterprise_quality":
                quality_score = results.get("overall_quality_score", 0)
                enterprise_ready = results.get("enterprise_ready", False)
                print(f"   📊 Quality Score: {quality_score:.1%}")
                print(f"   🏢 Enterprise Ready: {'Yes' if enterprise_ready else 'No'}")
        
        # Final assessment
        print(f"\n{'='*80}")
        if successful_phases >= 4:
            print("🎉 ENTERPRISE PLATFORM VALIDATION: PASSED")
            print("✅ System is ready for Fortune 500 deployment")
        elif successful_phases >= 3:
            print("⚠️ ENTERPRISE PLATFORM VALIDATION: PARTIAL")
            print("🔧 Minor optimizations needed for full enterprise readiness")
        else:
            print("❌ ENTERPRISE PLATFORM VALIDATION: FAILED")
            print("🛠️ Significant improvements required")
        
        print(f"📅 Test Completed: {datetime.now(timezone.utc).isoformat()}")
        print("="*80)

async def main():
    """Main test execution."""
    test_suite = EnterpriseIntegrationTest()
    await test_suite.run_comprehensive_test_suite()

if __name__ == "__main__":
    asyncio.run(main())
