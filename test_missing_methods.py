#!/usr/bin/env python3
"""
Test script to identify missing methods in enterprise agents
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_missing_methods():
    """Test for missing methods in enterprise agents"""
    
    try:
        print("Testing Enterprise Content Manager Agent...")
        from agents.website_agents.content_manager.content_agent_enterprise import EnterpriseContentManagerAgent
        content_agent = EnterpriseContentManagerAgent()
        await content_agent.initialize()
        
        # Test the missing method
        test_request = {
            "business_type": "professional_services",
            "region": {"country": "US"}
        }
        
        try:
            result = await content_agent.handle_request(test_request)
            print("✅ Content Manager: All methods working")
        except AttributeError as e:
            print(f"❌ Content Manager missing method: {e}")
        except Exception as e:
            print(f"⚠️ Content Manager other error: {e}")
            
    except Exception as e:
        print(f"❌ Content Manager import error: {e}")
    
    try:
        print("\nTesting Enterprise SEO Optimizer Agent...")
        from agents.website_agents.seo_optimizer.seo_agent_enterprise import EnterpriseSEOOptimizerAgent
        seo_agent = EnterpriseSEOOptimizerAgent()
        await seo_agent.initialize()
        
        test_request = {
            "business_type": "professional_services",
            "region": {"country": "US"},
            "target_markets": ["US", "UK"]
        }
        
        try:
            result = await seo_agent.handle_request(test_request)
            print("✅ SEO Optimizer: All methods working")
        except AttributeError as e:
            print(f"❌ SEO Optimizer missing method: {e}")
        except Exception as e:
            print(f"⚠️ SEO Optimizer other error: {e}")
            
    except Exception as e:
        print(f"❌ SEO Optimizer import error: {e}")
    
    try:
        print("\nTesting Enterprise Social Media Agent...")
        from agents.marketing_agents.social_media.social_agent_enterprise import EnterpriseSocialMediaAgent
        social_agent = EnterpriseSocialMediaAgent()
        await social_agent.initialize()
        
        test_request = {
            "business_type": "professional_services",
            "region": {"country": "US"},
            "target_markets": ["US", "UK"]
        }
        
        try:
            result = await social_agent.handle_request(test_request)
            print("✅ Social Media: All methods working")
        except AttributeError as e:
            print(f"❌ Social Media missing method: {e}")
        except Exception as e:
            print(f"⚠️ Social Media other error: {e}")
            
    except Exception as e:
        print(f"❌ Social Media import error: {e}")
    
    try:
        print("\nTesting Enterprise Quality Control Agent...")
        from agents.core_agents.quality_control.quality_agent_enterprise import EnterpriseQualityControlAgent
        quality_agent = EnterpriseQualityControlAgent()
        await quality_agent.initialize()
        
        test_agent_outputs = {
            "content_manager": {"website_content": {"homepage": "test content"}},
            "seo_optimizer": {"keywords": ["test"]},
            "social_media": {"platforms": ["linkedin"]}
        }
        
        try:
            result = await quality_agent.evaluate_agent_outputs(test_agent_outputs)
            print("✅ Quality Control: All methods working")
        except AttributeError as e:
            print(f"❌ Quality Control missing method: {e}")
        except Exception as e:
            print(f"⚠️ Quality Control other error: {e}")
            
    except Exception as e:
        print(f"❌ Quality Control import error: {e}")

if __name__ == "__main__":
    asyncio.run(test_missing_methods())
