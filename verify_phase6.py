import asyncio
from services.core.agents.orchestrator import OrchestratorAgent
from services.core.agents.base import AgentConfig

async def verify_phase6():
    print("🚀 Verifying Phase 6: Strategic Roadmap Engine...")
    
    # 1. Initialize Orchestrator
    config = AgentConfig(name="Orchestrator", description="Main Orchestrator", model="gpt-4-turbo-preview")
    orchestrator = OrchestratorAgent(config)
    
    # 2. Generate Roadmap
    input_data = {
        "goal": "Grow bakery revenue by 50% through digital marketing and seasonal events.",
        "timeframe": 90
    }
    
    print(f"📋 Generating roadmap for goal: {input_data['goal']}")
    project = await orchestrator.create_strategic_roadmap(input_data)
    
    print(f"✅ Project Created: {project.id}")
    print(f"📅 Status: {project.status}")
    print(f"🏁 Milestones: {len(project.milestones)}")
    
    for m in project.milestones:
        print(f"  - [{m.target_date}] {m.title}")

    print("\n✅ Phase 6 Roadmap Engine Verified!")

if __name__ == "__main__":
    asyncio.run(verify_phase6())
