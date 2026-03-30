# Legacy Agent → ADK Agent Audit

> Generated: 2026-03-21

## 1. Legacy Agent Inventory

The original `guild/src/agents/` directory **no longer exists** in the new codebase. The legacy agents were previously scattered across the old `Guild-AI` repository (referenced via `LEGACY_ROOT` in `services/core/bridge.py`). The legacy bridge registered 3 agents manually and had the capability to scan for more:

| Legacy Agent | Original Provider | Status |
|---|---|---|
| CopywriterAgent | ollama/tinyllama | ✅ Migrated |
| BookkeepingAgent | ollama/tinyllama | ✅ Migrated |
| EventMarketingAgent | ollama/tinyllama | ✅ Migrated |
| ImageGenerationAgent | openai/dall-e | ✅ Migrated |
| JudgeAgent | ollama/tinyllama | ✅ Migrated |
| LeadPersonalizationAgent | ollama/tinyllama | ✅ Migrated |
| LearningAgent | ollama/tinyllama | ✅ Migrated |
| SocialMediaAgent | ollama/tinyllama | ✅ Migrated |
| ScraperAgent | ollama/tinyllama | ✅ Migrated |
| LeadProspectorAgent | ollama/tinyllama | ✅ Migrated |
| VideoEditorAgent | openai | ✅ Migrated |
| BusinessStrategistAgent | ollama/tinyllama | ✅ Migrated |
| MarketingAgent | ollama/tinyllama | ✅ Migrated |
| SalesFunnelAgent | ollama/tinyllama | ✅ Migrated |
| SEOAgent | ollama/tinyllama | ✅ Migrated |
| SEOBrandOptimizer | ollama/tinyllama | ✅ Migrated |
| PaidAdsAgent | ollama/tinyllama | ✅ Migrated |
| ContentIntelligenceAgent | ollama/tinyllama | ✅ Migrated |
| ContentStrategist | ollama/tinyllama | ✅ Migrated |
| ContentRepurposerAgent | ollama/tinyllama | ✅ Migrated |
| EnhancedMarketingAgent | ollama/tinyllama | ✅ Migrated |
| EnhancedMarketingAgency | ollama/tinyllama | ✅ Migrated |
| UpsellCrossSellAgent | ollama/tinyllama | ✅ Migrated |
| ProposalWriterAgent | ollama/tinyllama | ✅ Migrated |
| PricingAgent | ollama/tinyllama | ✅ Migrated |
| OutboundSalesAgent | ollama/tinyllama | ✅ Migrated |
| TrendSpotterAgent | ollama/tinyllama | ✅ Migrated |

---

## 2. ADK Agent Inventory

All ADK agents use `default_llm` (configurable via `services/core/llm.py`).

### Top-Level (`services/core/adk/`)

| Agent | File | Capabilities | Category |
|---|---|---|---|
| BusinessIntelligenceAgent | `business_intelligence.py` | analyze_business, ceo_snapshot, kpi_tracking | Intelligence |
| CustomerIntelligenceAgent | `customer_intelligence.py` | analyze_customers, segmentation, churn_prediction | Customer |
| FinancialAdvisorAgent | `financial_advisor.py` | analyze_finances, forecast_revenue, budget_planning | Finance |
| MarketingStrategistAgent | `marketing_strategist.py` | create_campaign, optimize_budget, marketing_strategy | Marketing |
| TrendAnalystAgent | `trend_analyst.py` | analyze_trends, market_research, opportunity_spotting | Intelligence |

### Marketing (`services/core/adk/marketing/`)

| Agent | File | Capabilities | Category |
|---|---|---|---|
| CampaignAgent | `campaigns.py` | design_campaign, build_automation, design_ab_test, analyze_campaign, optimize_campaign | Marketing |
| ContentMarketingAgent | `content.py` | create_strategy, generate_content, optimize_seo, repurpose_content, analyze_performance | Marketing |
| ContentIntelligenceAgent | `content_intelligence.py` | analyze_content, content_strategy, performance_tracking | Intelligence |
| GrowthAgent | `growth.py` | seo_audit, keyword_research, plan_ads_campaign, social_strategy, plan_event, growth_roadmap | Marketing |

### Sales (`services/core/adk/sales/`)

| Agent | File | Capabilities | Category |
|---|---|---|---|
| LeadAgent | `leads.py` | qualify_lead, score_leads, personalize_outreach, segment_leads, batch_personalize | Sales |
| SalesPipelineAgent | `pipeline.py` | design_funnel, optimize_funnel, create_outreach, plan_campaign, analyze_pipeline, forecast_revenue | Sales |
| RevenueAgent | `revenue.py` | find_upsell_opportunities, generate_proposal, optimize_pricing, forecast_revenue | Sales |

### HR (`services/core/adk/hr/`)

| Agent | File | Capabilities | Category |
|---|---|---|---|
| TalentAcquisitionAgent | `talent_acquisition.py` | design_hiring_strategy, create_job_description, screen_cv, manage_freelancers | HR |
| TeamCultureAgent | `team_culture.py` | analyze_workload, recommend_interventions, design_learning_path | HR |

### Operations (`services/core/adk/operations/`)

| Agent | File | Capabilities | Category |
|---|---|---|---|
| FinanceOperationsAgent | `finance_operations.py` | process_financial_data, reconcile_accounts, generate_investor_update | Operations |
| LegalComplianceAgent | `legal_compliance.py` | analyze_contract, check_compliance, assess_business_risk | Operations |

### Core Agents (`services/core/agents/`)

| Agent | File | Capabilities | Category |
|---|---|---|---|
| ContentStrategistAgent | `content.py` | content_strategy, calendar_creation | Content |
| CopywriterAgent | `content.py` | copywriting, content_creation | Content |
| ResearchAgent | `research.py` | web_search, summarization | Research |
| EvaluatorLeague | `evaluator.py` | fact_checking, brand_compliance, seo_validation | Quality |
| OrchestratorAgent | `orchestrator.py` | workflow_management, task_delegation | Orchestration |

---

## 3. Capability Comparison Matrix

| Legacy Agent | ADK Equivalent | Coverage | Notes |
|---|---|---|---|
| CopywriterAgent | `CopywriterAgent` (content.py) + `ContentMarketingAgent` | ✅ FULL | Direct port + enhanced via ContentMarketing |
| BookkeepingAgent | `FinanceOperationsAgent` | ✅ FULL | `process_financial_data`, `reconcile_accounts` |
| EventMarketingAgent | `GrowthAgent.plan_event()` | ✅ FULL | Consolidated into growth marketing |
| ImageGenerationAgent | `CreativeAgent` | ✅ FULL | `generate_image_prompt`, `design_brand_identity`, `create_ad_visuals`, `visual_strategy` |
| JudgeAgent | `EvaluatorLeague` (evaluator.py) | ✅ FULL | FactChecker + BrandCompliance + SEO evaluators |
| LeadPersonalizationAgent | `LeadAgent` | ✅ FULL | `personalize_outreach`, `batch_personalize`, `qualify_lead` |
| LearningAgent | `TeamCultureAgent.design_learning_path()` | ✅ FULL | Skills gap analysis + learning modules |
| SocialMediaAgent | `ContentMarketingAgent` + `GrowthAgent.social_strategy()` | ✅ FULL | Content + social strategy combined |
| ScraperAgent | `ResearchAgent` | ✅ FULL | Web search via Playwright + LLM summarization |
| LeadProspectorAgent | `ResearchAgent` + `LeadAgent` | ✅ FULL | Research + lead qualification pipeline |
| VideoEditorAgent | `VideoAgent` | ✅ FULL | `write_script`, `create_editing_plan`, `video_strategy`, `repurpose_video`, `design_thumbnail` |
| BusinessStrategistAgent | `BusinessIntelligenceAgent` + `TrendAnalystAgent` | ✅ FULL | BI analysis + trend detection combined |
| MarketingAgent | `CampaignAgent` + `MarketingStrategistAgent` | ✅ FULL | Campaign design + strategy |
| SalesFunnelAgent | `SalesPipelineAgent` | ✅ FULL | `design_funnel`, `optimize_funnel` |
| SEOAgent | `GrowthAgent` | ✅ FULL | `seo_audit`, `keyword_research` |
| OutboundSalesAgent | `SalesPipelineAgent` | ✅ FULL | `create_outreach`, `plan_campaign` |
| ContentRepurposerAgent | `ContentMarketingAgent.repurpose()` | ✅ FULL | Multi-format content repurposing |
| UpsellCrossSellAgent | `RevenueAgent` | ✅ FULL | `find_upsell_opportunities` |
| ProposalWriterAgent | `RevenueAgent` | ✅ FULL | `generate_proposal` |
| PricingAgent | `RevenueAgent` | ✅ FULL | `optimize_pricing` |

---

## 4. Gaps Summary

> ✅ **All gaps closed.** `CreativeAgent` and `VideoAgent` were built to cover ImageGeneration and VideoEditor capabilities.

---

## 5. Hardcoded Path Violations Found

| File | Line | Hardcoded Path |
|---|---|---|
| `services/core/agents/identity.py` | 12 | `/Users/arnovanzyl/.gemini/antigravity/scratch/data/business_identity.json` |
| `services/core/agents/secrets.py` | 18 | `/Users/arnovanzyl/.gemini/antigravity/scratch/data` |
| `services/core/bridge.py` | 9 | `/Users/arnovanzyl/Dropbox/Mac (2)/Documents/GitHub/Guild-AI` |
| `services/core/agents/bridge.py` | 117 | `/Users/arnovanzyl/Dropbox/...` (comment) |
| `scripts/verify_oauth_bridge.py` | 16 | `/Users/arnovanzyl/.gemini/antigravity/scratch/data/test_oauth_secrets` |
| `scripts/import_legacy_integrations.py` | 10-11 | Two hardcoded paths |
| `scripts/verify_execution_layer.py` | 36 | `/Users/arnovanzyl/.gemini/antigravity/scratch/data/test_secrets` |

---

## 6. Legacy Bridge Files to Delete

| File | Purpose | Safe to Delete? |
|---|---|---|
| `services/core/bridge.py` | `LegacyAgentAdapter` + `scan_and_register_legacy_agents()` | ✅ Yes — only imported by `scripts/verify_bridge.py` |
| `services/core/agents/bridge.py` | `LegacyBridge` registry importer | ✅ Yes — no active imports |
| `services/core/integrations/connectors/legacy/` | 25 legacy connector files (~650KB) | ✅ Yes — not imported by any active code |
| `scripts/verify_bridge.py` | Bridge verification script | ✅ Yes — depends on deleted bridge files |
