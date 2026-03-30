from typing import Any, Dict, List, Optional
from datetime import datetime
import json
from pydantic import BaseModel, Field

from services.core.agents.base import BaseAgent
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm
from services.core.utils.json_extractor import extract_json_from_llm_response

# --- Data Models ---

class TrendSignal(BaseModel):
    source: str
    category: str
    signal: str
    strength: float
    recency_days: int
    region: Optional[str] = None
    link: Optional[str] = None

class TrendInsight(BaseModel):
    theme: str
    summary: str
    implications: List[str]
    opportunities: List[str]
    risks: List[str]
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.now)

# --- Agent Implementation ---

class TrendAnalystAgent(BaseAgent):
    """
    Trend Analyst Agent
    Detects and synthesizes emerging trends into actionable insights.
    Ported from legacy TrendSpotterAgent.
    """
    
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command", "analyze_trends")
        
        if command == "analyze_trends":
            return await self.run_trend_analysis(input_data, context)
        else:
            return await self.run_trend_analysis(input_data, context)

    async def run_trend_analysis(self, input_data: Dict[str, Any], context: Optional[Dict] = None):
        try:
            self.logger.info("Starting comprehensive trend analysis...")
            
            # Setup context parameters
            focus_domains = input_data.get("focus_domains", ["General Market"])
            business_objectives = input_data.get("business_objectives", {})
            
            # Simulate or fetch data sources (In future, use ResearchAgent here)
            data_sources = {
                "social": ["X/Twitter", "LinkedIn"],
                "news": ["TechCrunch", "Bloomberg"],
                "reports": ["Gartner", "McKinsey"]
            }
            
            # 1. Generate Strategy via LLM
            trend_strategy = await self._generate_trend_strategy(focus_domains, data_sources, business_objectives)
            
            # 2. Execute Workflow (Simulated signal processing)
            execution_result = await self._execute_trend_workflow(trend_strategy)
            
            return {
                "agent": "TrendAnalystAgent",
                "strategy_type": "comprehensive_trend_detection",
                "trend_strategy": trend_strategy,
                "execution_result": execution_result,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
            
        except Exception as e:
            self.logger.error(f"Trend analysis failed: {e}", exc_info=True)
            return {"error": str(e)}

    async def _generate_trend_strategy(self, focus_domains: List[str], data_sources: Dict, objectives: Dict) -> Dict:
        """Generates comprehensive trend strategy using LLM."""
        sys_prompt = self.build_system_prompt("You are the Trend Analyst Agent, an expert in detecting emerging market and cultural trends.", {})
        user_prompt = f"""
        **Focus Domains:** {json.dumps(focus_domains)}
        **Data Sources:** {json.dumps(data_sources)}
        **Business Objectives:** {json.dumps(objectives)}
        
        **Task:**
        Synthesize weak signals, group them into themes, and produce actionable insights.
        
        **Output Format (JSON):**
        Return a JSON object with keys: 'signals' (list), 'themes' (list), 'insights' (list), 'roadmap' (object).
        For 'signals', include source, signal description, and strength (0-1).
        For 'themes', include name, summary, and confidence.
        For 'insights', include theme, implications, opportunities, and risks.
        
        Think step by step extracting high-level themes from the provided sources."""
        
        try:
            response = await default_llm.chat_completion([
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ])
            return self._extract_json(response)
        except Exception as e:
            self.logger.error(f"LLM strategy generation failed: {e}")
            return {"error": "Failed to generate strategy via LLM", "details": str(e)}

    async def _execute_trend_workflow(self, strategy: Dict) -> Dict:
        """Execute the trend workflow (Simulated for migration)."""
        
        signals = self._normalize_signals(strategy.get("signals", []))
        themes = self._cluster_themes(strategy.get("themes", []), signals)
        insights = self._derive_insights(themes, signals) # Use LLM generated insights if available, else derive
        
        # If LLM provided insights directly, use them, otherwise use derived ones
        llm_insights = strategy.get("insights", [])
        if llm_insights:
            final_insights = llm_insights
        else:
            final_insights = [i.dict() for i in insights]

        return {
            "processed_signals_count": len(signals),
            "themes_identified": len(themes),
            "insights": final_insights,
            "roadmap": strategy.get("roadmap", {})
        }

    def _normalize_signals(self, raw_signals: List[Dict]) -> List[TrendSignal]:
        """Normalize signal data."""
        normalized = []
        for sig in raw_signals:
            try:
                normalized.append(TrendSignal(
                    source=sig.get("source", "unknown"),
                    category=sig.get("category", "general"),
                    signal=sig.get("signal", ""),
                    strength=float(sig.get("strength", 0.5)),
                    recency_days=int(sig.get("recency_days", 30))
                ))
            except Exception:
                continue
        return normalized

    def _cluster_themes(self, theme_specs: List[Dict], signals: List[TrendSignal]) -> List[Dict]:
        """Cluster signals into themes (Simulated/Pass-through)."""
        # In a full implementation, this might use vector similarity
        return theme_specs

    def _derive_insights(self, themes: List[Dict], signals: List[TrendSignal]) -> List[TrendInsight]:
        """Derive insights from themes (Simulated/Pass-through)."""
        insights = []
        for theme in themes:
            insights.append(TrendInsight(
                theme=theme.get("name", "Unnamed"),
                summary=theme.get("summary", ""),
                implications=theme.get("implications", []),
                opportunities=theme.get("opportunities", []),
                risks=theme.get("risks", []),
                confidence=float(theme.get("confidence", 0.5))
            ))
        return insights

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "error": "Failed to analyze trends",
            "signals": [],
            "themes": [],
            "insights": [],
            "roadmap": {}
        }

    def _extract_json(self, text: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(text, fallback=self._get_fallback_response())

# Register Result
AgentRegistry.register(AgentCapability(
    name="TrendAnalystAgent",
    category="Intelligence",
    capabilities=["analyze_trends", "market_research", "opportunity_spotting"],
    description="Detects emerging market trends and synthesizes actionable insights.",
    agent_class=TrendAnalystAgent
))
