import asyncio
from services.core.agents.orchestrator import OrchestratorAgent
from services.core.agents.base import AgentConfig
from services.core.agents.models import DelegationPlan, DelegationSpec, AuthorityLevel, TaskStatus
from services.core.agents.authorization import auth_queue

async def verify_phase7():
    print("🚀 Verifying Phase 7: Authorize & Execute Loop...")
    
    # 1. Initialize Orchestrator
    config = AgentConfig(name="Orchestrator", description="Main Orchestrator", model="gpt-4-turbo-preview")
    orchestrator = OrchestratorAgent(config)
    
    # 2. Create a Mock Plan with a HUMAN-level task
    mock_plan = DelegationPlan(tasks=[
        DelegationSpec(
            id="task_1",
            intent="Post a holiday discount update to Instagram.",
            assigned_agent="content_strategist",
            rationale="Strategic post requirements.",
            authority_level=AuthorityLevel.HUMAN, # Human in the loop!
            risk_level="medium"
        )
    ])
    
    # 3. Execute implementation loop
    print("⏳ Executing plan with Human-in-the-loop task...")
    results = await orchestrator._execute_plan(mock_plan, {})
    
    # 4. Check if task is PENDING and in Auth Queue
    task_res = results.get("task_1", {})
    if task_res.get("auth_required"):
        print(f"✅ Task paused successfully. Auth ID: {task_res['auth_id']}")
        
        pending_reqs = auth_queue.list_pending()
        print(f"📝 Items in Auth Queue: {len(pending_reqs)}")
        if len(pending_reqs) > 0:
            print(f"✅ Auth Request found: {pending_reqs[0].description}")
    else:
        print("❌ Task did not pause for authorization.")

    print("\n✅ Phase 7 Authorization Loop Verified!")

if __name__ == "__main__":
    asyncio.run(verify_phase7())
