import asyncio
import json
from services.core.agents.orchestrator import OrchestratorAgent
from services.core.agents.base import AgentConfig
from services.core.agents.registry import AgentRegistry

async def verify_delegation():
    print("🚀 Starting Intelligence Delegation Verification (Enhanced)...")
    
    # 1. Setup Orchestrator
    config = AgentConfig(name="OrchestratorAgent", description="Test Orchestrator")
    orchestrator = OrchestratorAgent(config)
    
    # 2. Test Goal
    goal = "Create a comprehensive content strategy for a new AI productivity tool."
    
    print(f"\nPrompting Orchestrator with goal: '{goal}'")
    
    # 3. Mock LLM Response
    async def mock_chat_completion(messages, temperature=0.7):
        return json.dumps({
            "tasks": [
                {
                    "id": "research_1",
                    "intent": "Research top 3 AI productivity tools...",
                    "assigned_agent": "ResearchAgent",
                    "dependencies": [],
                    "boundaries": ["No video tools"],
                    "authority_level": "full",
                    "success_criteria": ["List of 3 tools"],
                    "rationale": "Specialized web search.",
                    "risk_level": "low",
                    "deadline": "short-term",
                    "resources": {"max_tokens": 1000},
                    "retry_limit": 1
                },
                {
                    "id": "strategy_1",
                    "intent": "Develop a content strategy...",
                    "assigned_agent": "ContentStrategistAgent",
                    "dependencies": ["research_1"],
                    "boundaries": ["Focus on differentiation"],
                    "authority_level": "semi",
                    "success_criteria": ["Content pillars defined"],
                    "rationale": "Tactical planning expert.",
                    "risk_level": "medium",
                    "deadline": "mid-term",
                    "resources": {"max_tokens": 2000},
                    "retry_limit": 2
                }
            ]
        })

    # Apply the patch
    from services.core.llm import default_llm
    default_llm.chat_completion = mock_chat_completion

    # 4. Mock Evaluator League
    from services.core.agents.evaluator import evaluator_league
    async def mock_review(task, output):
        print(f"🧐 Evaluator League reviewing: {task.id} (Risk: {task.risk_level})")
        return {"approved": True, "feedback": ""}
    evaluator_league.review = mock_review

    try:
        result = await orchestrator.process({"goal": goal})
        
        print("\n✅ Plan Generated & Executed Successfully!")
        plan = result.get("plan", {})
        tasks = plan.get("tasks", [])
        
        for task in tasks:
            print(f"\n--- Task: {task.get('id')} ---")
            print(f"Risk: {task.get('risk_level')}")
            print(f"Deadline: {task.get('deadline')}")
            print(f"Resources: {task.get('resources')}")
            print(f"Retry Limit: {task.get('retry_limit')}")
            
        print("\n✅ Verification Complete!")
        
    except Exception as e:
        print(f"\n❌ Verification Failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    async def main():
        # Ensure agents are registered
        from services.core.agents.research import ResearchAgent
        from services.core.agents.content import ContentStrategistAgent, CopywriterAgent
        
        await verify_delegation()
        
    asyncio.run(main())
