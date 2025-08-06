"""
Debug test to see exact response structure from orchestrator.
"""

import asyncio
import json
import sys
import os

project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

from agents.core_agents.orchestrator.master_orchestrator import GlobalMasterOrchestrator

async def debug_response():
    print("🔍 DEBUG: Checking exact response structure...")
    
    orchestrator = GlobalMasterOrchestrator()
    await orchestrator.initialize()
    
    result = await orchestrator.process_request({
        "business_name": "Debug Test",
        "location": "London, UK", 
        "description": "Debug test in London",
        "request_type": "complete_automation"
    })
    
    print("📋 Response keys:")
    for key in result.keys():
        print(f"   - {key}")
    
    print("\n📋 Results keys:")
    if "results" in result:
        for key in result["results"].keys():
            print(f"   - {key}")
    
    # Check specific keys
    keys_to_check = ["region_context", "business_analysis", "business_context", "location_data"]
    for key in keys_to_check:
        if key in result:
            print(f"✅ Found {key}")
        else:
            print(f"❌ Missing {key}")
    
    # Save debug output
    with open("debug_response.json", "w") as f:
        json.dump(result, f, indent=2, default=str)
    print("\n📁 Full response saved to debug_response.json")

if __name__ == "__main__":
    asyncio.run(debug_response())
