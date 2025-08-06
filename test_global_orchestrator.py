from agents.core_agents.orchestrator.master_orchestrator import GlobalMasterOrchestrator
import asyncio
import json

async def test_global_detection():
    orchestrator = GlobalMasterOrchestrator()
    
    # Initialize the orchestrator first
    print("🔄 Initializing Global Master Orchestrator...")
    await orchestrator.initialize()
    print("✅ Orchestrator initialized successfully!")
    
    # Test the user's specific examples
    test_cases = [
        'I need help setting up a Pizza shop in New York',
        'I want to open a Boutique in London', 
        'Help me start a Restaurant in Dubai',
        'Building a tech startup in Singapore',
        'Opening a cafe in Mumbai'
    ]
    
    for test_case in test_cases:
        print(f'\n=== Testing: {test_case} ===')
        try:
            result = await orchestrator.process_request({
                'description': test_case,  # Changed from 'request' to 'description'
                'business_type': 'restaurant' if 'pizza' in test_case.lower() or 'restaurant' in test_case.lower() or 'cafe' in test_case.lower() else 'retail'
            })
            
            print(f"Full result keys: {list(result.keys())}")
            
            # Print location detection results
            if 'detected_market' in result:
                market = result['detected_market']
                location_info = market.get('location', {})
                print(f"✅ Location: {location_info.get('city', 'Unknown')} ({location_info.get('country', 'Unknown')})")
                print(f"✅ Market Tier: {market.get('market_tier', 'Unknown')}")
                
                # Print pricing from market_pricing
                if 'market_pricing' in result:
                    pricing = result['market_pricing']
                    packages = pricing.get('monthly_packages', {})
                    print(f"💰 Pricing Packages: {packages}")
                
                # Print cultural events from cultural_intelligence
                if 'cultural_intelligence' in result:
                    cultural = result['cultural_intelligence']
                    events = cultural.get('cultural_events', [])[:2]
                    event_names = [e.get('name') for e in events]
                    print(f"🎉 Key Cultural Events: {event_names}")
            
            elif 'detected_location' in result:
                loc = result['detected_location']
                location_info = loc.get('location', {})
                print(f"✅ Location: {location_info.get('city', 'Unknown')} ({location_info.get('country', 'Unknown')})")
                print(f"✅ Market Tier: {loc.get('market_tier', 'Unknown')}")
                
                # Print pricing
                if 'pricing_tier' in loc:
                    pricing = loc['pricing_tier']
                    packages = pricing.get('monthly_packages', {})
                    print(f"💰 Pricing Packages: {packages}")
                
                # Print cultural events
                if 'cultural_events' in loc:
                    events = loc['cultural_events'][:2]  # First 2 events
                    event_names = [e.get('name') for e in events]
                    print(f"🎉 Key Cultural Events: {event_names}")
            else:
                print("❌ No detected_location found in result")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_global_detection())
