from .business_intelligence import BusinessIntelligenceAgent
from .customer_intelligence import CustomerIntelligenceAgent
from .financial_advisor import FinancialAdvisorAgent
from .marketing_strategist import MarketingStrategistAgent
from .trend_analyst import TrendAnalystAgent

# Sub-packages (Marketing, Sales, HR, Operations, Customer)
from . import marketing
from . import sales
from . import hr
from . import operations
from . import customer  # CRMAgent

# Import non-ADK core agents that need registration at startup
from services.core.agents import judge  # JudgeAgent
from services.core.calendar import engine as calendar_engine  # CalendarHarmonyAgent

def register_all_agents():
    """
    Called to ensure all ADK agents are imported and registered.
    """
    # Imports above already trigger registration via AgentRegistry.register decorator/call
    pass

__all__ = [
    "BusinessIntelligenceAgent",
    "CustomerIntelligenceAgent",
    "FinancialAdvisorAgent",
    "MarketingStrategistAgent",
    "TrendAnalystAgent",
    "register_all_agents"
]
