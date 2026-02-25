import asyncio
from services.core.agents.evaluator import evaluator_league
from services.core.agents.models import DelegationSpec

async def main():
    task = DelegationSpec(
        id="test-task-1",
        intent="Write a short paragraph about the current CEO of Google. Ensure it is factually correct, uses professional brand voice, and is optimized for SEO.",
        assigned_agent="ContentAgent",
        rationale="For testing purposes",
        success_criteria=[
            "Must mention Sundar Pichai",
            "Must be professional",
            "Must use keywords: Google, CEO, Alphabet"
        ]
    )
    
    # A deliberately flawed output to see if the evaluators catch it
    bad_output = """
    The current CEO of Google is Larry Page. He is doing a terrible job and everyone hates him. 
    """
    
    print("Evaluating bad output...")
    res1 = await evaluator_league.review(task, bad_output)
    print("Result:", res1)
    print("-" * 40)
    
    # A good output
    good_output = """
    Sundar Pichai is the current CEO of Google and its parent company, Alphabet. Under his leadership, Google continues to innovate in AI and cloud computing, maintaining a highly professional standard across the industry.
    """
    
    print("Evaluating good output...")
    res2 = await evaluator_league.review(task, good_output)
    print("Result:", res2)

if __name__ == "__main__":
    asyncio.run(main())
