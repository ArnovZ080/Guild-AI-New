from typing import Any, Dict, List, Optional
from services.core.agents.base import BaseAgent
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm
from services.core.utils.json_extractor import extract_json_from_llm_response
import json

class FinanceOperationsAgent(BaseAgent):
    """
    Finance Operations Agent
    Consolidates legacy Accounting and Investor Relations functionalities.
    """
    
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command")
        
        if command == "process_financial_data":
            return await self.process_financial_data(input_data, context)
        elif command == "reconcile_accounts":
            return await self.reconcile_accounts(input_data, context)
        elif command == "generate_investor_update":
            return await self.generate_investor_update(input_data, context)
        else:
            raise ValueError(f"Unknown command for FinanceOperationsAgent: {command}")

    async def process_financial_data(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate P&L, balance sheets, and expense reports from raw transactions."""
        transactions = input_data.get("transactions", [])
        period = input_data.get("period", "Current Month")
        
        sys_prompt = self.build_system_prompt("You are an expert Corporate Accountant. Process the raw transactions into structured financial reports.", context)
        user_prompt = f"""
        **Period:** {period}
        **Transactions Count:** {len(transactions)}
        
        Analyze the following financial data and return a JSON report including P&L summary, major expense categories, and anomalies:
        {json.dumps(transactions[:50])}  # Truncated for token limits in this implementation
        
        **Response Format:**
        {{
            "profit_loss": {{"revenue": 10000, "cogs": 2000, "gross_profit": 8000, "operating_expenses": 3000, "net_profit": 5000}},
            "expense_breakdown": [{{"category": "string", "amount": 100, "percentage": 10}}],
            "anomalies": ["string"],
            "financial_health_score": 85
        }}
        
        Think step by step compiling revenue vs expenses."""
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    async def reconcile_accounts(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Automate bookkeeping and catch discrepancies between internal books and bank statements."""
        internal_records = input_data.get("internal_records", [])
        bank_statements = input_data.get("bank_statements", [])
        
        sys_prompt = self.build_system_prompt("You are a specialized Reconciliation Accountant.", context)
        user_prompt = f"""
        Compare the internal records against the bank statements and identify any discrepancies.
        Internal Records Count: {len(internal_records)}
        Bank Statement Count: {len(bank_statements)}
        
        **Response Format:**
        {{
            "reconciliation_status": "matched|discrepancies_found|needs_review",
            "discrepancies": [
                {{"transaction_id": "string", "internal_amount": 100, "bank_amount": 100, "reason": "string"}}
            ],
            "suggested_adjustments": ["string"]
        }}
        
        Think step by step carefully comparing records."""
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    async def generate_investor_update(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Compile financial metrics and operational updates for stakeholders."""
        metrics = input_data.get("financial_metrics", {})
        highlights = input_data.get("operational_highlights", [])
        challenges = input_data.get("challenges", [])
        
        sys_prompt = self.build_system_prompt("You are the Director of Investor Relations. Draft an engaging, transparent investor update.", context)
        user_prompt = f"""
        Draft an investor update using the provided details.
        
        **Financial Metrics:**
        {json.dumps(metrics)}
        
        **Operational Highlights:**
        {json.dumps(highlights)}
        
        **Challenges & Mitigation:**
        {json.dumps(challenges)}
        
        **Response Format:**
        {{
            "subject_line": "string",
            "executive_summary": "string",
            "financial_update": "string",
            "operational_update": "string",
            "challenges_and_asks": "string",
            "closing": "string"
        }}
        
        Think step by step on structuring the narrative."""
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "error": "Failed to complete finance operations request",
            "profit_loss": {"revenue": 0, "cogs": 0, "gross_profit": 0, "operating_expenses": 0, "net_profit": 0},
            "expense_breakdown": [],
            "anomalies": [],
            "financial_health_score": 0,
            "reconciliation_status": "needs_review",
            "discrepancies": [],
            "suggested_adjustments": [],
            "subject_line": "Financial Update",
            "executive_summary": "Report failed.",
            "financial_update": "Data unavailable."
        }

    def _extract_json(self, text: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(text, fallback=self._get_fallback_response())

AgentRegistry.register(AgentCapability(
    name="FinanceOperationsAgent",
    category="Operations",
    capabilities=["process_financial_data", "reconcile_accounts", "generate_investor_update"],
    description="Handles corporate accounting, reconciliation, and investor relations reporting.",
    agent_class=FinanceOperationsAgent
))
