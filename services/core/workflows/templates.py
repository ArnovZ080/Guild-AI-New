"""
Pre-built Workflow Templates — Phase 2.
Fixes agent name references and adds flywheel-specific templates.
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
        .add_step("Generate Welcome Content", "CopywriterAgent", "create_onboarding_sequence",
                   params={"customer_id": "{customer_id}"},
                   dependencies=["Enrich Profile"])
        .add_step("Schedule Welcome Emails", "CopywriterAgent", "send_email_sequence",
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
        .add_step("Sentiment Analysis", "ContentIntelligenceAgent", "analyze_sentiment",
                   params={"customer_id": "{customer_id}"},
                   dependencies=["Analyze Customer Health"])
        .add_step("Generate Retention Strategy", "BusinessIntelligenceAgent", "retention_strategy",
                   params={"customer_id": "{customer_id}", "health": "{health_data}"},
                   risk_level=RiskLevel.MEDIUM,
                   dependencies=["Sentiment Analysis"])
        .add_step("Create Retention Offer", "CopywriterAgent", "create_retention_content",
                   params={"customer_id": "{customer_id}", "strategy": "{strategy}"},
                   dependencies=["Generate Retention Strategy"])
        .add_step("Execute Outreach", "CopywriterAgent", "send_retention_campaign",
                   params={"customer_id": "{customer_id}"},
                   risk_level=RiskLevel.HIGH,
                   dependencies=["Create Retention Offer"])
    )

    # ─────────── Content Workflows ───────────

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="content_campaign",
            display_name="Multi-Channel Content Campaign",
            description="Research → Create → Judge → Publish across all channels.",
            category="content",
        )
        .add_step("Research Topic", "ResearchAgent", "research_topic",
                   params={"topic": "{topic}", "audience": "{target_audience}"})
        .add_step("Create Content", "ContentMarketingAgent", "create_content",
                   params={"topic": "{topic}", "research": "{research}"},
                   dependencies=["Research Topic"])
        .add_step("Quality Review", "JudgeAgent", "evaluate_content",
                   params={"content": "{content}"},
                   risk_level=RiskLevel.MEDIUM,
                   dependencies=["Create Content"])
        .add_step("Publish to Social", "ContentMarketingAgent", "distribute",
                   params={"content": "{content}", "platforms": "{platforms}"},
                   risk_level=RiskLevel.LOW,
                   dependencies=["Quality Review"])
        .add_step("Schedule Email Blast", "CopywriterAgent", "send_newsletter",
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
        .add_step("Qualify Lead", "CRMAgent", "score_lead",
                   params={"lead_id": "{lead_id}", "source": "{source}"})
        .add_step("Enrich Lead Data", "ResearchAgent", "enrich_lead",
                   params={"lead_id": "{lead_id}"},
                   dependencies=["Qualify Lead"])
        .add_step("Generate Personalized Pitch", "CopywriterAgent", "create_pitch",
                   params={"lead_id": "{lead_id}", "profile": "{enriched_profile}"},
                   dependencies=["Enrich Lead Data"])
        .add_step("Send Outreach", "CopywriterAgent", "send_outreach",
                   params={"lead_id": "{lead_id}", "pitch": "{pitch}"},
                   risk_level=RiskLevel.LOW,
                   dependencies=["Generate Personalized Pitch"])
        .add_step("Schedule Follow-up", "CalendarHarmonyAgent", "schedule_content",
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
        .add_step("Generate Report", "CopywriterAgent", "create_financial_report",
                   params={"analysis": "{trend_analysis}"},
                   dependencies=["Analyze Trends"])
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
        .add_step("Generate Strategic Brief", "CopywriterAgent", "create_strategy_brief",
                   params={"analysis": "{market_analysis}"},
                   dependencies=["Analyze Market Position"])
    )

    # ─────────── Master Workflows ───────────

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="grand_opening",
            display_name="Strategic Business Launch",
            description="End-to-end launch: Research → Plan → Brand → Launch.",
            category="master",
        )
        .add_step("Market & Competitor Analysis", "ResearchAgent", "competitive_research",
                   params={"focus": "new_business_launch"})
        .add_step("Generate Strategic Business Plan", "BusinessIntelligenceAgent", "generate_roadmap",
                   params={"market_data": "{market_data}"},
                   dependencies=["Market & Competitor Analysis"])
        .add_step("Create Brand Hero Content", "ContentMarketingAgent", "create_brand_identity",
                   params={"business_plan": "{business_plan}"},
                   dependencies=["Generate Strategic Business Plan"])
        .add_step("Setup Lead Acquisition Funnel", "CRMAgent", "add_contact",
                   params={"brand_assets": "{brand_assets}"},
                   dependencies=["Create Brand Hero Content"])
        .add_step("Global Launch Review", "JudgeAgent", "evaluate_content",
                   params={"launch_package": "{full_package}"},
                   risk_level=RiskLevel.CRITICAL,
                   dependencies=["Setup Lead Acquisition Funnel"])
        .add_step("Execute Go-to-Market Distribution", "ContentMarketingAgent", "distribute_launch",
                   params={"package": "{approved_package}"},
                   risk_level=RiskLevel.HIGH,
                   dependencies=["Global Launch Review"])
    )

    # ═══════════ NEW FLYWHEEL TEMPLATES ═══════════

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="weekly_content_pipeline",
            display_name="Weekly Content Pipeline",
            description="Full weekly flywheel: analyze → strategize → create → judge → schedule.",
            category="content",
        )
        .add_step("Analyze Last Week Performance", "ContentIntelligenceAgent", "analyze_performance",
                   params={"period": "last_week"})
        .add_step("Generate Content Strategy", "ContentMarketingAgent", "create_strategy",
                   params={"performance": "{performance_data}"},
                   dependencies=["Analyze Last Week Performance"])
        .add_step("Create Text Content Batch", "CopywriterAgent", "batch_create",
                   params={"strategy": "{strategy}"},
                   dependencies=["Generate Content Strategy"])
        .add_step("Create Visual Content", "CreativeAgent", "generate_visuals",
                   params={"content_batch": "{text_content}"},
                   dependencies=["Generate Content Strategy"])
        .add_step("Create Video Content", "VideoAgent", "generate_videos",
                   params={"strategy": "{strategy}"},
                   dependencies=["Generate Content Strategy"])
        .add_step("Quality Review All Items", "JudgeAgent", "evaluate_content",
                   params={"content": "{all_content}"},
                   risk_level=RiskLevel.MEDIUM,
                   dependencies=["Create Text Content Batch", "Create Visual Content", "Create Video Content"])
        .add_step("Schedule to Calendar", "CalendarHarmonyAgent", "schedule_content",
                   params={"approved_content": "{approved_items}"},
                   dependencies=["Quality Review All Items"])
    )

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="lead_capture_qualification",
            display_name="Lead Capture & Qualification",
            description="Capture engagement, score ICP, enrich, assign nurture.",
            category="sales",
        )
        .add_step("Capture Engagement Data", "CRMAgent", "add_contact",
                   params={"engagement": "{engagement_data}"})
        .add_step("Score Against ICP", "LeadAgent", "score_lead",
                   params={"contact_id": "{contact_id}"},
                   dependencies=["Capture Engagement Data"])
        .add_step("Enrich Contact Profile", "ResearchAgent", "enrich_lead",
                   params={"contact_id": "{contact_id}"},
                   dependencies=["Capture Engagement Data"])
        .add_step("Assign Nurture Sequence", "CopywriterAgent", "create_nurture_content",
                   params={"contact_id": "{contact_id}", "profile": "{enriched_profile}"},
                   dependencies=["Score Against ICP", "Enrich Contact Profile"])
    )

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="product_launch_campaign",
            display_name="Product Launch Campaign",
            description="Full launch: research → strategy → content → ads → email → schedule → launch.",
            category="master",
        )
        .add_step("Research Market Positioning", "ResearchAgent", "market_research",
                   params={"product": "{product_info}"})
        .add_step("Analyze Trends", "TrendAnalystAgent", "analyze_trends",
                   params={"market": "{market_data}"},
                   dependencies=["Research Market Positioning"])
        .add_step("Create Campaign Strategy", "CampaignAgent", "plan_campaign",
                   params={"research": "{research}", "trends": "{trend_data}"},
                   dependencies=["Research Market Positioning", "Analyze Trends"])
        .add_step("Generate All Content Formats", "ContentMarketingAgent", "create_campaign_content",
                   params={"strategy": "{campaign_strategy}"},
                   dependencies=["Create Campaign Strategy"])
        .add_step("Create Visual & Video Assets", "CreativeAgent", "generate_campaign_assets",
                   params={"content": "{content}"},
                   dependencies=["Create Campaign Strategy"])
        .add_step("Quality Review", "JudgeAgent", "evaluate_content",
                   params={"content": "{all_content}"},
                   risk_level=RiskLevel.HIGH,
                   dependencies=["Generate All Content Formats", "Create Visual & Video Assets"])
        .add_step("Build Landing Page Copy", "CopywriterAgent", "create_landing_page",
                   params={"campaign": "{campaign_strategy}"},
                   dependencies=["Create Campaign Strategy"])
        .add_step("Create Email Sequence", "CopywriterAgent", "create_email_sequence",
                   params={"campaign": "{campaign_strategy}"},
                   dependencies=["Quality Review"])
        .add_step("Schedule Everything", "CalendarHarmonyAgent", "schedule_content",
                   params={"content": "{all_items}"},
                   dependencies=["Quality Review", "Create Email Sequence", "Build Landing Page Copy"])
    )

    WorkflowExecutor.register_template(
        WorkflowTemplate(
            name="monthly_growth_review",
            display_name="Monthly Growth Review",
            description="Aggregate metrics, analyze pipeline, review nurture conversions, recommend adjustments.",
            category="operations",
        )
        .add_step("Aggregate Content Performance", "ContentIntelligenceAgent", "monthly_summary",
                   params={"period": "last_month"})
        .add_step("Analyze Lead Pipeline", "CRMAgent", "get_pipeline_summary",
                   params={"period": "last_month"})
        .add_step("Review Nurture Conversions", "CustomerIntelligenceAgent", "conversion_analysis",
                   params={"period": "last_month"},
                   dependencies=["Analyze Lead Pipeline"])
        .add_step("Generate Insights Report", "BusinessIntelligenceAgent", "comprehensive_report",
                   params={"content_data": "{content_perf}", "pipeline": "{pipeline}", "conversions": "{conversions}"},
                   dependencies=["Aggregate Content Performance", "Analyze Lead Pipeline", "Review Nurture Conversions"])
        .add_step("Recommend Strategy Adjustments", "GrowthAgent", "recommend_adjustments",
                   params={"report": "{insights_report}"},
                   dependencies=["Generate Insights Report"])
    )
