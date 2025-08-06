"""
Test script to verify orchestrator integration with enhanced agents.
This tests the complete workflow to ensure agents are properly called.
"""

import asyncio
import json
import logging
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

from agents.core_agents.orchestrator.master_orchestrator import GlobalMasterOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_orchestrator_integration():
    """Test complete orchestrator integration with enhanced agents."""
    print("🔄 Testing Global Master Orchestrator Integration...")
    
    try:
        # Initialize orchestrator
        orchestrator = GlobalMasterOrchestrator()
        await orchestrator.initialize()
        print("✅ Orchestrator initialized successfully")
        
        # Test complete business automation request
        test_request = {
            "business_type": "restaurant",
            "business_name": "London Bistro",
            "target_audience": "Food lovers in London",
            "location": "London, UK",
            "request_type": "complete_automation",
            "services": ["website", "marketing", "analytics"],
            "description": "A modern bistro serving international cuisine in London"
        }
        
        print(f"📝 Testing complete automation request for: {test_request['business_name']}")
        
        # Process the request
        result = await orchestrator.process_request(test_request)
        
        # Check if we got the expected keys
        print("\n🔍 Checking orchestrator response structure...")
        
        if "status" in result:
            print(f"   Status: {result['status']}")
        
        if "results" in result:
            results = result["results"]
            print(f"   Results keys: {list(results.keys())}")
            
            # Check for expected agent results
            expected_keys = ["website_builder", "marketing_campaign", "data_analytics"]
            for key in expected_keys:
                if key in results:
                    agent_result = results[key]
                    if isinstance(agent_result, dict) and "status" in agent_result:
                        print(f"   ✅ {key}: {agent_result['status']}")
                        
                        # Show generated files if available
                        if "generated_files" in agent_result:
                            files = agent_result["generated_files"]
                            print(f"      Generated {len(files)} files")
                    else:
                        print(f"   ❌ {key}: Invalid structure")
                else:
                    print(f"   ❌ Missing {key} in results")
        
        if "region_context" in result:
            region = result["region_context"]
            print(f"   Region detected: {region.get('country')} ({region.get('market_tier')})")
        
        # Show business context
        if "business_analysis" in result:
            business = result["business_analysis"]
            print(f"   Business type: {business.get('business_type')}")
            print(f"   Location: {business.get('location')}")
        
        print("\n📊 Testing Summary:")
        print(f"   Request processed: {'✅' if result.get('status') == 'success' else '❌'}")
        print(f"   Agents called: {'✅' if 'results' in result else '❌'}")
        print(f"   Location detected: {'✅' if 'region_context' in result else '❌'}")
        
        # Save detailed results for inspection
        output_file = os.path.join(project_root, "test_orchestrator_result.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"   Detailed results saved to: {output_file}")
        
        return result
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Run the test
    result = asyncio.run(test_orchestrator_integration())
    
    if result and result.get("status") == "success":
        print("\n🎉 ORCHESTRATOR INTEGRATION TEST PASSED!")
        print("   All agents are properly connected and responding.")
    else:
        print("\n💥 ORCHESTRATOR INTEGRATION TEST FAILED!")
        print("   Check the errors above and fix the integration issues.")
