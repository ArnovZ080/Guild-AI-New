"""
Pre-built Workflow Templates.
These are the autonomous multi-step workflows that run the business.
Each template chains agents together for end-to-end automation.
"""
from .models import WorkflowTemplate, RiskLevel
from .executor import WorkflowExecutor


def register_all_templates():
    """Register all pre-built workflow templates."""

    # ─────────── Customer Workflows ───────────

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="customer_onboarding",
            display_name="Customer Onboarding Automation",
            description="Automated welcome sequence with profile enrichment and personalized content.",
            category="customer",
        )
        .add_step("Create Customer Profile", "CustomerIntelligenceAgent", "create_profile",
                   params={"customer_id": "{customer_id}", "data": "{customer_data}"})
        .add_step("Enrich Profile", "ResearchAgent", "enrich_customer_profile",
                   params={"customer_id": "{customer_id}"},
                   dependencies=["Create Customer Profile"])
        .add_step("Generate Welcome Content", "ContentAgent", "create_onboarding_sequence",
                   params={"customer_id": "{customer_id}"},
                   dependencies=["Enrich Profile"])
        .add_step("Schedule Welcome Emails", "CommunicationBridge", "send_email_sequence",
                   params={"customer_id": "{customer_id}"},
                   risk_level=RiskLevel.LOW,
                   dependencies=["Generate Welcome Content"])
    )

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="customer_retention",
            display_name="Customer Retention Campaign",
            description="Detect at-risk customers, analyze sentiment, create personalized retention offers.",
            category="customer",
        )
        .add_step("Analyze Customer Health", "CustomerIntelligenceAgent", "analyze_health",
                   params={"customer_id": "{customer_id}"})
        .add_step("Sentiment Analysis", "ContentAgent", "analyze_sentiment",
                   params={"customer_id": "{customer_id}"},
                   dependencies=["Analyze Customer Health"])
        .add_step("Generate Retention Strategy", "BusinessIntelligenceAgent", "retention_strategy",
                   params={"customer_id": "{customer_id}", "health": "{health_data}"},
                   risk_level=RiskLevel.MEDIUM,
                   dependencies=["Sentiment Analysis"])
        .add_step("Create Retention Offer", "ContentAgent", "create_retention_content",
                   params={"customer_id": "{customer_id}", "strategy": "{strategy}"},
                   dependencies=["Generate Retention Strategy"])
        .add_step("Execute Outreach", "CommunicationBridge", "send_retention_campaign",
                   params={"customer_id": "{customer_id}"},
                   risk_level=RiskLevel.HIGH,
                   dependencies=["Create Retention Offer"])
    )

    # ─────────── Content Workflows ───────────

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="content_campaign",
            display_name="Multi-Channel Content Campaign",
            description="Research → Create → Review → Publish across all channels.",
            category="content",
        )
        .add_step("Research Topic", "ResearchAgent", "research_topic",
                   params={"topic": "{topic}", "audience": "{target_audience}"})
        .add_step("Create Content", "ContentAgent", "create_content",
                   params={"topic": "{topic}", "research": "{research}"},
                   dependencies=["Research Topic"])
        .add_step("Quality Review", "EvaluatorLeague", "review_content",
                   params={"content": "{content}"},
                   risk_level=RiskLevel.MEDIUM,
                   dependencies=["Create Content"])
        .add_step("Publish to Social", "SocialBridge", "distribute",
                   params={"content": "{content}", "platforms": "{platforms}"},
                   risk_level=RiskLevel.LOW,
                   dependencies=["Quality Review"])
        .add_step("Schedule Email Blast", "CommunicationBridge", "send_newsletter",
                   params={"content": "{content}", "segment": "{audience_segment}"},
                   risk_level=RiskLevel.MEDIUM,
                   dependencies=["Quality Review"])
    )

    # ─────────── Sales Workflows ───────────

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="lead_nurture",
            display_name="Lead Nurturing Sequence",
            description="Qualify, enrich, and nurture new leads through automated follow-up.",
            category="sales",
        )
        .add_step("Qualify Lead", "CustomerIntelligenceAgent", "qualify_lead",
                   params={"lead_id": "{lead_id}", "source": "{source}"})
        .add_step("Enrich Lead Data", "ResearchAgent", "enrich_lead",
                   params={"lead_id": "{lead_id}"},
                   dependencies=["Qualify Lead"])
        .add_step("Generate Personalized Pitch", "ContentAgent", "create_pitch",
                   params={"lead_id": "{lead_id}", "profile": "{enriched_profile}"},
                   dependencies=["Enrich Lead Data"])
        .add_step("Send Outreach", "CommunicationBridge", "send_outreach",
                   params={"lead_id": "{lead_id}", "pitch": "{pitch}"},
                   risk_level=RiskLevel.LOW,
                   dependencies=["Generate Personalized Pitch"])
        .add_step("Schedule Follow-up", "CalendarBridge", "schedule_followup",
                   params={"lead_id": "{lead_id}", "days_delay": 3},
                   dependencies=["Send Outreach"])
    )

    # ─────────── Financial Workflows ───────────

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="financial_review",
            display_name="Monthly Financial Review",
            description="Aggregate financials, analyze trends, generate executive summary.",
            category="finance",
        )
        .add_step("Aggregate Financial Data", "FinancialAdvisorAgent", "aggregate_financials",
                   params={"period": "{period}"})
        .add_step("Analyze Trends", "BusinessIntelligenceAgent", "analyze_financial_trends",
                   params={"data": "{financial_data}"},
                   dependencies=["Aggregate Financial Data"])
        .add_step("Generate Report", "ContentAgent", "create_financial_report",
                   params={"analysis": "{trend_analysis}"},
                   dependencies=["Analyze Trends"])
        .add_step("Send to Executive", "CommunicationBridge", "send_report",
                   params={"report": "{report}", "recipient": "{executive_email}"},
                   risk_level=RiskLevel.MEDIUM,
                   dependencies=["Generate Report"])
    )

    # ─────────── Operations Workflows ───────────

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="competitive_intel",
            display_name="Competitive Intelligence Sweep",
            description="Research competitors, analyze positioning, update strategy.",
            category="operations",
        )
        .add_step("Research Competitors", "ResearchAgent", "competitive_research",
                   params={"competitors": "{competitor_list}", "focus": "{focus_areas}"})
        .add_step("Analyze Market Position", "BusinessIntelligenceAgent", "market_analysis",
                   params={"research": "{competitor_data}"},
                   dependencies=["Research Competitors"])
        .add_step("Generate Strategic Brief", "ContentAgent", "create_strategy_brief",
                   params={"analysis": "{market_analysis}"},
                   dependencies=["Analyze Market Position"])
        .add_step("Update Strategy Dashboard", "BusinessIntelligenceAgent", "update_dashboard",
                   params={"brief": "{strategy_brief}"},
                   dependencies=["Generate Strategic Brief"])
    )

    # ─────────── Master Workflows (Multi-Domain) ───────────

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="grand_opening",
            display_name="Strategic Business Launch",
            description="End-to-end launch sequence: Market Research → Business Plan → Brand Identity → Social Launch.",
            category="master",
        )
        .add_step("Market & Competitor Analysis", "ResearchAgent", "competitive_research",
                   params={"focus": "new_business_launch"})
        .add_step("Generate Strategic Business Plan", "BusinessIntelligenceAgent", "generate_roadmap",
                   params={"market_data": "{market_data}"},
                   dependencies=["Market & Competitor Analysis"])
        .add_step("Create Brand Hero Content", "ContentAgent", "create_brand_identity",
                   params={"business_plan": "{business_plan}"},
                   dependencies=["Generate Strategic Business Plan"])
        .add_step("Setup Lead Acquisition Funnel", "CustomerIntelligenceAgent", "setup_funnel",
                   params={"brand_assets": "{brand_assets}"},
                   dependencies=["Create Brand Hero Content"])
        .add_step("Global Launch Review", "EvaluatorLeague", "final_compliance_check",
                   params={"launch_package": "{full_package}"},
                   risk_level=RiskLevel.CRITICAL,
                   dependencies=["Setup Lead Acquisition Funnel"])
        .add_step("Execute Go-to-Market Distribution", "SocialBridge", "distribute_launch",
                   params={"package": "{approved_package}"},
                   risk_level=RiskLevel.HIGH,
                   dependencies=["Global Launch Review"])
    )
