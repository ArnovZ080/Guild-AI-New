from typing import Any, Dict, List, Optional
from services.core.agents.base import BaseAgent
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm
from services.core.utils.json_extractor import extract_json_from_llm_response
import json

class LegalComplianceAgent(BaseAgent):
    """
    Legal & Compliance Agent
    Consolidates legacy Risk Management, Compliance, and Contract Analyzer functionalities.
    """
    
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command")
        
        if command == "analyze_contract":
            return await self.analyze_contract(input_data, context)
        elif command == "check_compliance":
            return await self.check_compliance(input_data, context)
        elif command == "assess_business_risk":
            return await self.assess_business_risk(input_data, context)
        else:
            raise ValueError(f"Unknown command for LegalComplianceAgent: {command}")

    async def analyze_contract(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Extract terms, obligations, and identify risks in legal documents."""
        contract_text = input_data.get("contract_text", "")
        party_name = input_data.get("party_name", "Our Company")
        
        sys_prompt = self.build_system_prompt("You are a Senior Corporate Lawyer. Analyze the contract and highlight obligations and risks.", context)
        user_prompt = f"""
        **Our Party Name:** {party_name}
        
        **Contract Text Extract:**
        {contract_text[:4000]} # Truncated for context limits
        
        **Response Format:**
        {{
            "contract_type": "string",
            "key_terms": ["string"],
            "our_obligations": ["string"],
            "counterparty_obligations": ["string"],
            "risks_identified": [
                {{"risk_level": "high|medium|low", "description": "string", "clause_reference": "string"}}
            ],
            "negotiation_recommendations": ["string"]
        }}
        
        Think step by step assessing each paragraph for potential liabilities."""
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    async def check_compliance(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Verify operations against regulatory frameworks like GDPR, HIPAA, or SOC2."""
        framework = input_data.get("framework", "GDPR")
        operational_data = input_data.get("operational_data", {})
        
        sys_prompt = self.build_system_prompt(f"You are a highly acclaimed {framework} Compliance Auditor.", context)
        user_prompt = f"""
        Review the following operational data and privacy policies against {framework} requirements.
        
        **Operational Data:**
        {json.dumps(operational_data)}
        
        **Response Format:**
        {{
            "compliance_status": "compliant|non_compliant|needs_review",
            "violations_found": [
                {{"severity": "critical|high|medium|low", "description": "string", "remediation": "string"}}
            ],
            "audit_score": 50
        }}
        
        Think step by step aligning practices against regulatory articles."""
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    async def assess_business_risk(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Evaluate operational, market, and financial risks to produce mitigation plans."""
        business_context = context or {}
        market_conditions = input_data.get("market_conditions", {})
        internal_vulnerabilities = input_data.get("internal_vulnerabilities", [])
        
        sys_prompt = self.build_system_prompt("You are a Chief Risk Officer. Identify holistic business risks and formulate mitigation strategies.", context)
        user_prompt = f"""
        **Business Context:** {json.dumps(business_context.get('business', 'Unknown'))}
        **Market Conditions:** {json.dumps(market_conditions)}
        **Internal Vulnerabilities:** {json.dumps(internal_vulnerabilities)}
        
        **Response Format:**
        {{
            "overall_risk_profile": "conservative|moderate|aggressive|critical",
            "key_risks": [
                {{"category": "market|operational|financial|cyber", "description": "string", "impact": "high|medium|low", "probability": "high|medium|low"}}
            ],
            "mitigation_plan": [
                {{"risk": "string", "strategy": "string", "timeline": "string"}}
            ]
        }}
        
        Think step by step through impact scenarios."""
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "error": "Failed to complete legal compliance request",
            "contract_type": "Unknown",
            "key_terms": [],
            "our_obligations": [],
            "counterparty_obligations": [],
            "risks_identified": [],
            "negotiation_recommendations": [],
            "compliance_status": "needs_review",
            "violations_found": [],
            "audit_score": 0,
            "overall_risk_profile": "critical",
            "key_risks": [],
            "mitigation_plan": []
        }

    def _extract_json(self, text: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(text, fallback=self._get_fallback_response())

AgentRegistry.register(AgentCapability(
    name="LegalComplianceAgent",
    category="Operations",
    capabilities=["analyze_contract", "check_compliance", "assess_business_risk"],
    description="Handles legal contract analysis, regulatory compliance auditing, and holistic business risk assessment.",
    agent_class=LegalComplianceAgent
))
