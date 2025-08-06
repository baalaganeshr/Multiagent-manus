"""
Quick test to verify London location detection fix.
"""

import asyncio
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

from agents.core_agents.orchestrator.master_orchestrator import GlobalMasterOrchestrator

async def quick_test():
    print("🔄 Quick test of London location detection...")
    orchestrator = GlobalMasterOrchestrator()
    await orchestrator.initialize()
    
    result = await orchestrator.process_request({
        "business_name": "Quick Test Bistro",
        "location": "London, UK", 
        "description": "Testing bistro in London",
        "request_type": "complete_automation"
    })
    
    if "results" in result and "website_builder" in result["results"]:
        website_result = result["results"]["website_builder"]
        business_info = website_result.get("business_info", {})
        location = business_info.get("location", {})
        print(f"✅ City detected: {location.get('city')}")
        print(f"✅ Country detected: {location.get('country')}")
        print(f"✅ State detected: {location.get('state')}")
    else:
        print("❌ No website builder result found")
        print(f"Available keys: {list(result.get('results', {}).keys())}")

if __name__ == "__main__":
    asyncio.run(quick_test())
