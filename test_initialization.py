from agents.core_agents.orchestrator.master_orchestrator import GlobalMasterOrchestrator
import asyncio

async def test_initialization():
    try:
        print("🔄 Creating GlobalMasterOrchestrator...")
        orchestrator = GlobalMasterOrchestrator()
        
        print("🔄 Initializing agents...")
        await orchestrator.initialize()
        
        print("✅ Success! Available agents:")
        for agent_name in orchestrator.agents.keys():
            print(f"  - {agent_name}")
        
        print(f"📊 Total agents initialized: {len(orchestrator.agents)}")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_initialization())
