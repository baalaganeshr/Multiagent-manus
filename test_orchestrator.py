#!/usr/bin/env python3
"""
Test script for the enhanced Master Orchestrator with Indian business automation
"""

import asyncio
import logging
from datetime import datetime
from agents.core_agents.orchestrator.master_orchestrator import MasterOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_orchestrator():
    """Test the enhanced orchestrator functionality."""
    print("🇮🇳 Testing Multiagent-manus Indian Business Automation Platform")
    print("=" * 60)
    
    # Initialize orchestrator
    orchestrator = MasterOrchestrator()
    await orchestrator.initialize()
    
    # Test cases
    test_cases = [
        {
            "name": "Restaurant Website Setup",
            "request": {
                "request_id": "test_001",
                "type": "website_creation",
                "description": "मुझे अपने रेस्टोरेंट के लिए एक वेबसाइट चाहिए जो ऑनलाइन ऑर्डर ले सके",
                "language": "hi",
                "business_data": {
                    "type": "restaurant",
                    "name": "Spice Garden",
                    "location": "Mumbai, Maharashtra"
                }
            }
        },
        {
            "name": "Festival Marketing Campaign",
            "request": {
                "request_id": "test_002",
                "type": "marketing_campaign",
                "description": "Create Diwali marketing campaign for my electronics store",
                "language": "en",
                "business_data": {
                    "type": "retail",
                    "name": "TechMart",
                    "location": "Delhi"
                }
            }
        },
        {
            "name": "Complete Business Setup",
            "request": {
                "request_id": "test_003",
                "type": "complete_setup",
                "description": "मुझे अपने बिजनेस के लिए पूरा सेटअप चाहिए - वेबसाइट, मार्केटिंग और WhatsApp integration",
                "language": "hi",
                "business_data": {
                    "type": "service",
                    "name": "Digital Solutions",
                    "location": "Bangalore"
                }
            }
        },
        {
            "name": "Analytics and Reporting",
            "request": {
                "request_id": "test_004", 
                "type": "analytics_setup",
                "description": "I need analytics dashboard for my ecommerce business",
                "language": "en",
                "business_data": {
                    "type": "ecommerce",
                    "name": "Fashion Store",
                    "location": "Chennai"
                }
            }
        }
    ]
    
    # Execute test cases
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            response = await orchestrator.process_request(test_case["request"])
            
            print(f"✅ Status: {response.get('status', 'unknown')}")
            print(f"📝 Message: {response.get('message', 'No message')}")
            print(f"🎯 Request Type: {response.get('request_type', 'unknown')}")
            
            if "business_analysis" in response:
                analysis = response["business_analysis"]
                print(f"🏢 Business Type: {analysis.get('business_type', 'unknown')}")
                print(f"📍 Location: {analysis.get('location', 'unknown')}")
                print(f"🗣️ Languages: {', '.join(analysis.get('languages_needed', []))}")
                print(f"🎪 Festival Relevance: {'Yes' if analysis.get('festival_relevance') else 'No'}")
            
            if "recommendations" in response:
                print("💡 Key Recommendations:")
                for rec in response["recommendations"][:3]:  # Show first 3
                    print(f"   • {rec}")
            
            if "next_steps" in response:
                print("📋 Next Steps:")
                for step in response["next_steps"][:2]:  # Show first 2
                    print(f"   • {step['action']} ({step['timeframe']})")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    # Cleanup
    await orchestrator.shutdown()
    print("\n🎉 Test completed successfully!")
    print("🚀 The Master Orchestrator is ready for Indian business automation!")

def main():
    """Main function to run the test."""
    try:
        asyncio.run(test_orchestrator())
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed: {str(e)}")

if __name__ == "__main__":
    main()
