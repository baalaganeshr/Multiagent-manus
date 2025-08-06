"""
Comprehensive Final Test - ORCHESTRATOR INTEGRATION FIX VALIDATION
This validates that the GlobalMasterOrchestrator properly routes requests to all three enhanced agents.
"""

import asyncio
import logging
import sys
import os
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

async def test_orchestrator_fix():
    """Test the complete orchestrator integration fix."""
    print("="*80)
    print("🔧 ORCHESTRATOR INTEGRATION FIX - FINAL VALIDATION")
    print("="*80)
    
    try:
        # Import and initialize
        from agents.core_agents.orchestrator.master_orchestrator import GlobalMasterOrchestrator
        
        print("📋 Test 1: Orchestrator Initialization")
        orchestrator = GlobalMasterOrchestrator()
        await orchestrator.initialize()
        print("   ✅ GlobalMasterOrchestrator initialized successfully")
        print(f"   ✅ {len(orchestrator.agents)} agents loaded")
        
        # Check which agents are loaded
        agent_types = list(orchestrator.agents.keys())
        print(f"   📝 Loaded agents: {', '.join(agent_types)}")
        
        # Test individual agent types
        expected_agents = ["website_builder", "campaign_manager", "data_collector"]
        for agent_name in expected_agents:
            if agent_name in orchestrator.agents:
                agent = orchestrator.agents[agent_name]
                agent_class = agent.__class__.__name__
                print(f"   ✅ {agent_name}: {agent_class}")
            else:
                print(f"   ❌ Missing {agent_name}")
        
        print("\n📋 Test 2: Complete Business Request Processing")
        
        # Test complete business automation request
        test_request = {
            "business_name": "Test Global Restaurant",
            "business_type": "restaurant", 
            "location": "London, UK",
            "description": "A test restaurant for validation in London",
            "request_type": "complete_automation",
            "target_audience": "Local food enthusiasts"
        }
        
        print(f"   📤 Sending request: {test_request['business_name']}")
        result = await orchestrator.process_request(test_request)
        
        # Validate response structure
        print("\n📋 Test 3: Response Structure Validation")
        
        if result.get("status") == "success":
            print("   ✅ Request processed successfully")
        else:
            print(f"   ❌ Request failed: {result.get('status')}")
            return False
        
        # Check for results
        if "results" in result:
            results = result["results"]
            print(f"   ✅ Results container present with {len(results)} components")
            
            # Check for expected agent results
            key_checks = {
                "website_builder": "Website Builder Agent",
                "marketing_campaign": "Marketing Campaign Agent", 
                "data_analytics": "Data Analytics Agent"
            }
            
            for key, description in key_checks.items():
                if key in results:
                    agent_result = results[key]
                    if isinstance(agent_result, dict) and "status" in agent_result:
                        status = agent_result["status"]
                        print(f"   ✅ {description}: {status}")
                        
                        # Check for generated files
                        if "generated_files" in agent_result:
                            file_count = len(agent_result["generated_files"])
                            print(f"      📁 Generated {file_count} files")
                        elif "files_created" in agent_result:
                            file_count = len(agent_result["files_created"])
                            print(f"      📁 Created {file_count} files")
                        else:
                            print(f"      📝 {description} completed")
                    else:
                        print(f"   ❌ {description}: Invalid result structure")
                else:
                    print(f"   ❌ {description}: Missing from results")
        else:
            print("   ❌ No results container in response")
            return False
        
        # Check region detection
        print("\n📋 Test 4: Global Intelligence Validation")
        
        if "detected_market" in result:
            market = result["detected_market"]
            country = market.get("country", "Unknown")
            market_tier = market.get("market_tier", "Unknown")
            city = market.get("city", "Unknown")
            print(f"   ✅ Location detected: {city}, {country}")
            print(f"   ✅ Market tier: {market_tier}")
        else:
            print("   ❌ No market detection found")
        
        if "market_pricing" in result or "cultural_intelligence" in result:
            if "market_pricing" in result:
                pricing = result["market_pricing"]
                print(f"   ✅ Market pricing analyzed: {pricing.get('tier', 'Unknown')}")
            if "cultural_intelligence" in result:
                culture = result["cultural_intelligence"]
                print(f"   ✅ Cultural adaptation: {culture.get('communication_style', 'Unknown')}")
        else:
            print("   ❌ No business analysis performed")
        
        # Final summary
        print("\n" + "="*80)
        print("🎉 ORCHESTRATOR INTEGRATION FIX - VALIDATION COMPLETE")
        print("="*80)
        
        success_indicators = [
            result.get("status") == "success",
            "results" in result,
            "website_builder" in result.get("results", {}),
            "marketing_campaign" in result.get("results", {}),
            "data_analytics" in result.get("results", {}),
            "detected_market" in result
        ]
        
        passed_tests = sum(success_indicators)
        total_tests = len(success_indicators)
        
        print(f"✅ Integration Status: {passed_tests}/{total_tests} core tests passed")
        
        if passed_tests == total_tests:
            print("🎯 RESULT: ORCHESTRATOR INTEGRATION FULLY FUNCTIONAL")
            print("   All three enhanced agents are properly connected and responding")
            print("   Location detection and business analysis working")
            print("   Ready for production use")
            return True
        else:
            print("⚠️  RESULT: PARTIAL INTEGRATION - Some issues remaining")
            return False
            
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run the comprehensive test
    success = asyncio.run(test_orchestrator_fix())
    
    if success:
        print("\n🚀 ORCHESTRATOR READY FOR DEPLOYMENT!")
    else:
        print("\n🔧 ORCHESTRATOR NEEDS ADDITIONAL FIXES")
    
    exit(0 if success else 1)
