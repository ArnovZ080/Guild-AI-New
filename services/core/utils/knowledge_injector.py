import json
from typing import Dict, Any, Optional

class KnowledgeInjector:
    """
    Retrieves and injects BusinessIdentity context, adaptive learning preferences,
    and integration data into an agent's prompt context.
    """

    @classmethod
    def get_business_context_prompt(cls, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Builds a markdown formatted block of business context.
        Uses provided context dict or fetches placeholder defaults.
        """
        if not context:
            context = {}

        # MOCK retrieval from databases/state for now
        business_identity = context.get('business_identity', {
            "name": "Acme Widgets",
            "industry": "B2B SaaS",
            "target_audience": "Mid-market software companies",
            "core_value_proposition": "We make workflow automation simple and affordable.",
            "brand_voice": "Professional but approachable. Confident, clear, no buzzwords."
        })

        adaptive_learning = context.get('adaptive_learning', [
            "User prefers concise summaries over long paragraphs.",
            "Always include ROI estimates when proposing strategies."
        ])

        integration_data = context.get('integration_data', {})

        lines = [
            "## Business Context & Identity",
            "You must ensure your output strictly aligns with the following business context.",
            "",
            "### Brand Identity",
            f"- **Company Name**: {business_identity.get('name', 'Unknown')}",
            f"- **Industry**: {business_identity.get('industry', 'Unknown')}",
            f"- **Target Audience**: {business_identity.get('target_audience', 'Unknown')}",
            f"- **Core Value Prop**: {business_identity.get('core_value_proposition', 'Unknown')}",
            f"- **Brand Voice**: {business_identity.get('brand_voice', 'Unknown')}",
            "",
            "### Adaptive Preferences (User/System wide)",
            "Follow these past preferences:"
        ]

        if adaptive_learning:
            for pref in adaptive_learning:
                lines.append(f"- {pref}")
        else:
            lines.append("- No specific learned preferences yet.")

        lines.append("")

        if integration_data:
            lines.append("### Connected Systems Data")
            for k, v in integration_data.items():
                lines.append(f"- **{k}**: {json.dumps(v)[:200]}...")
            lines.append("")

        return "\n".join(lines)
