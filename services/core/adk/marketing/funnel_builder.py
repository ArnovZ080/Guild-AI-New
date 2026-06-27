"""
Funnel Builder Agent — Generates complete HTML landing pages based on campaign requirements
and brand style guide context.
"""
from services.core.adk.base import BaseAgent
from services.core.agents.identity import BusinessIdentityManager
from typing import Dict, Any, Optional
import json

FUNNEL_PROMPT = """You are the FunnelBuilderAgent, an expert in creating high-converting, visually stunning landing pages.

Given the Business Context (including their brand style guide and colors), and the specific Campaign or Objective requested, generate a complete, standalone HTML page.

## Requirements:
1. Provide a COMPLETE, standalone HTML document (starting with <!DOCTYPE html>).
2. The page MUST look beautiful and professional. Use Tailwind CSS via CDN: `<script src="https://cdn.tailwindcss.com"></script>`.
3. In the `<head>`, include any necessary Google Fonts to match the brand style guide.
4. If a brand style guide is provided, strictly adhere to its colors, typography, and vibe. Apply the colors using Tailwind arbitrary values (e.g., `text-[#FF5733]`, `bg-[#1A1A1A]`).
5. Include a lead capture form.
6. **CRITICAL FORM REQUIREMENT**: The form MUST have `action="/api/public/form/{{form_id}}"` and `method="POST"`. (The backend will replace `{{form_id}}` with the actual ID).
7. Ensure responsive design (mobile-first).
8. Use FontAwesome (via CDN) or inline SVG icons to make it look premium.
9. Output ONLY valid HTML. Do not wrap in markdown code blocks like ```html ... ```. Just raw HTML starting with <!DOCTYPE html>.
10. Ensure the HTML is accessible and semantic.

## Output Format:
Return ONLY the raw HTML string. No commentary, no explanations.
"""

class FunnelBuilderAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="FunnelBuilderAgent",
            system_prompt=FUNNEL_PROMPT,
            **kwargs
        )

    async def generate_landing_page(self, user_id: str, objective: str, db=None) -> str:
        """Generates a landing page HTML string based on user context and objective."""
        # 1. Gather context
        context_prompt = ""
        if db:
            context_prompt = await BusinessIdentityManager.get_context_prompt(db, user_id)
            
        full_prompt = f\"\"\"
{context_prompt}

## Campaign / Objective
{objective}

Please generate the HTML for this landing page.
\"\"\"
        # 2. Call LLM
        response = await self.call_llm(full_prompt, temperature=0.7)
        
        html_content = response.strip()
        if html_content.startswith("```html"):
            html_content = html_content[7:]
        if html_content.startswith("```"):
            html_content = html_content[3:]
        if html_content.endswith("```"):
            html_content = html_content[:-3]
            
        return html_content.strip()
