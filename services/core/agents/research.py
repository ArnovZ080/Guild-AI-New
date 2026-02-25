from typing import Any, Dict, Optional
from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm
import logging

try:
    from playwright.async_api import async_playwright
except ImportError:
    async_playwright = None

class ResearchAgent(BaseAgent):
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        query = input_data.get("query") or input_data.get("objective") or input_data.get("intent")
        if not query:
            raise ValueError("ResearchAgent requires a 'query', 'objective', or 'intent' in input_data")
        
        self.logger.info(f"Researching: {query}")
        result = await self.search_web(query)
        return result

    async def search_web(self, query: str) -> Dict[str, Any]:
        if not async_playwright:
             return {"error": "Playwright not installed"}

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                # Basic DuckDuckGo search
                search_url = f"https://duckduckgo.com/?q={query}"
                await page.goto(search_url, wait_until="networkidle")
                
                # Extract first result (simplified for now)
                selector = 'a[data-testid="result-title-a"]'
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    first_link = await page.get_attribute(selector, 'href')
                    
                    if first_link:
                        await page.goto(first_link, wait_until="domcontentloaded")
                        content = await page.evaluate("document.body.innerText")
                        # Use LLM to summarize
                        summary = await self.summarize_content(query, content[:5000])
                        return {
                            "url": first_link,
                            "summary": summary
                        }
                except Exception as e:
                    self.logger.warning(f"Search selection failed: {e}")

                return {"url": search_url, "summary": "Search performed but content extraction failed."}

            finally:
                await browser.close()

    async def summarize_content(self, query: str, content: str) -> str:
        prompt = [
            {"role": "system", "content": "You are a research assistant. Summarize the following content relevant to the user's query."},
            {"role": "user", "content": f"Query: {query}\n\nContent:\n{content}"}
        ]
        return await default_llm.chat_completion(prompt)

# Register the agent
AgentRegistry.register(AgentCapability(
    name="ResearchAgent",
    category="Research",
    capabilities=["web_search", "summarization"],
    description="Performs web research and summaries findings.",
    agent_class=ResearchAgent
))
