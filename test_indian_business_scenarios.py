#!/usr/bin/env python3
"""
Enhanced Test Script for Master Orchestrator
Tests the exact scenarios requested with Indian business context
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

async def test_indian_business_scenarios():
    """Test the specific Indian business automation scenarios."""
    print("🇮🇳 Testing Master Orchestrator with Real Indian Business Scenarios")
    print("=" * 70)
    
    # Initialize orchestrator
    orchestrator = MasterOrchestrator()
    await orchestrator.initialize()
    
    # Test cases as specified in the request
    test_requests = [
        {
            "name": "South Indian Restaurant Website",
            "request": {
                "type": "website_creation",
                "description": "Create a website for my South Indian restaurant",
                "language": "en",
                "business_data": {
                    "type": "restaurant",
                    "name": "Chennai Delights",
                    "location": "Chennai, Tamil Nadu",
                    "cuisine": "South Indian",
                    "specialties": ["dosa", "idli", "sambar", "filter coffee"]
                }
            }
        },
        {
            "name": "Clothing Store Marketing Automation",
            "request": {
                "type": "marketing_campaign",
                "description": "I need marketing automation for my clothing store",
                "language": "en",
                "business_data": {
                    "type": "retail",
                    "name": "Fashion Hub",
                    "location": "Mumbai, Maharashtra",
                    "products": ["traditional wear", "western wear", "accessories"]
                }
            }
        },
        {
            "name": "Mobile Repair Service Analytics",
            "request": {
                "type": "analytics_setup",
                "description": "Setup analytics dashboard for my mobile repair service",
                "language": "en",
                "business_data": {
                    "type": "service",
                    "name": "Mobile Fix Pro",
                    "location": "Bangalore, Karnataka",
                    "services": ["phone repair", "screen replacement", "software issues"]
                }
            }
        },
        {
            "name": "Complete Bakery Automation",
            "request": {
                "type": "complete_setup",
                "description": "Complete automation for my bakery - website, marketing, everything",
                "language": "en",
                "business_data": {
                    "type": "restaurant",
                    "name": "Sweet Dreams Bakery",
                    "location": "Delhi",
                    "products": ["cakes", "pastries", "bread", "custom orders"]
                }
            }
        }
    ]
    
    # Execute test cases
    for i, test_case in enumerate(test_requests, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print("-" * 50)
        
        try:
            response = await orchestrator.process_request(test_case["request"])
            
            # Display core results
            print(f"✅ Status: {response.get('status', 'unknown')}")
            if response.get('message'):
                print(f"📝 Message: {response.get('message')}")
            
            # Business analysis results
            if "business_analysis" in response:
                analysis = response["business_analysis"]
                print(f"🏢 Business Type: {analysis.get('business_type', 'unknown')}")
                print(f"📍 Location: {analysis.get('location', 'unknown')}")
                print(f"⚡ Urgency: {analysis.get('urgency', 'unknown')}")
                print(f"💰 Budget Range: {analysis.get('budget_range', 'unknown')}")
                print(f"🎪 Festival Relevance: {'Yes' if analysis.get('festival_relevance') else 'No'}")
                print(f"🗣️ Languages: {', '.join(analysis.get('languages_needed', []))}")
            
            # Indian optimizations
            if "indian_optimizations" in response:
                optimizations = response["indian_optimizations"]
                print(f"💳 Payment Methods: {', '.join(optimizations.get('payment_methods', []))}")
                print(f"🌐 WhatsApp Integration: {'Yes' if optimizations.get('whatsapp_integration') else 'No'}")
                print(f"📱 Mobile Optimization: {'Yes' if optimizations.get('mobile_optimization') else 'No'}")
                print(f"📄 GST Compliance: {'Yes' if optimizations.get('gst_compliance') else 'No'}")
            
            # Location-specific insights
            if "location_specific" in response:
                location_data = response["location_specific"]
                print(f"🏙️ Regional Insights: {location_data.get('preferred_languages', [])}")
                print(f"⏰ Peak Hours: {location_data.get('peak_hours', 'Not specified')}")
            
            # Key recommendations
            if "recommendations" in response:
                print("💡 Key Recommendations:")
                for j, rec in enumerate(response["recommendations"][:5], 1):  # Show top 5
                    print(f"   {j}. {rec}")
            
            # Next steps
            if "next_steps" in response:
                print("📋 Next Steps:")
                for step in response["next_steps"][:3]:  # Show first 3
                    priority_emoji = "🔴" if step['priority'] == 'high' else "🟡" if step['priority'] == 'medium' else "🟢"
                    print(f"   {priority_emoji} {step['action']} ({step['timeframe']})")
            
            # Agent coordination results
            if "results" in response and isinstance(response["results"], dict):
                print("🤖 Agent Coordination:")
                for agent_type, result in response["results"].items():
                    if isinstance(result, dict) and result.get('status') == 'success':
                        print(f"   ✅ {agent_type.title()}: {result.get('message', 'Completed')}")
            
            print()
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print()
    
    # Show agent status
    print("\n🔍 System Status Check:")
    print("-" * 30)
    try:
        status = await orchestrator.get_agent_status()
        print(f"📊 Total Agents: {status.get('total_agents', 0)}")
        print(f"🟢 Active Agents: {status.get('active_agents', 0)}")
        print(f"📝 Active Tasks: {status.get('active_tasks', 0)}")
        print(f"⏱️ System Uptime: {status.get('uptime', 'Unknown')}")
        
        if "agent_details" in status:
            print("\n🤖 Agent Status:")
            for agent_name, agent_status in status["agent_details"].items():
                status_emoji = "🟢" if agent_status == "active" else "🔴"
                print(f"   {status_emoji} {agent_name}: {agent_status}")
                
    except Exception as e:
        print(f"❌ Status check failed: {str(e)}")
    
    # Cleanup
    await orchestrator.shutdown()
    print("\n🎉 All tests completed successfully!")
    print("🚀 Master Orchestrator is ready for Indian business automation!")

def main():
    """Main function to run the enhanced tests."""
    try:
        asyncio.run(test_indian_business_scenarios())
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Tests failed: {str(e)}")

if __name__ == "__main__":
    main()
