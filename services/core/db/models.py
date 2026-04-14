"""
Guild-AI Database Models — Master Instructions v2.0 Schema

All tables defined in Section 13 of GUILD_AI_MASTER_INSTRUCTIONS_v2.md.
Uses async PostgreSQL via asyncpg.
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime,
    ForeignKey, Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base


def generate_uuid():
    return str(uuid.uuid4())


# ── Core ──

class UserAccount(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    firebase_uid = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    role = Column(String, default="user")
    subscription_tier = Column(String, default="free")  # free, starter, growth, scale
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    business_identity = relationship("BusinessIdentity", back_populates="user", uselist=False)
    conversations = relationship("Conversation", back_populates="user")
    content_items = relationship("ContentItem", back_populates="user")
    contacts = relationship("Contact", back_populates="user")
    campaigns = relationship("Campaign", back_populates="user")
    workflows = relationship("Workflow", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    calendar_events = relationship("CalendarEvent", back_populates="user")
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    connected_integrations = relationship("ConnectedIntegration", back_populates="user")
    knowledge_documents = relationship("KnowledgeDocument", back_populates="user")
    token_usage = relationship("TokenUsage", back_populates="user")
    media_assets = relationship("MediaAsset", back_populates="user")


class BusinessIdentity(Base):
    __tablename__ = "business_identity"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    business_name = Column(String, nullable=True)
    niche = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    target_audience = Column(Text, nullable=True)
    icp = Column(JSONB, default=dict)              # Detailed ICP with psychographics
    brand_voice = Column(JSONB, default=dict)       # voice, tone, vocabulary, do's/don'ts
    brand_visual = Column(JSONB, default=dict)      # colors, fonts, imagery style
    brand_story = Column(Text, nullable=True)
    competitors = Column(JSONB, default=list)
    pricing_strategy = Column(Text, nullable=True)
    marketing_channels = Column(JSONB, default=list)
    content_preferences = Column(JSONB, default=dict)  # formats, topics, frequency
    goals_3month = Column(Text, nullable=True)
    goals_12month = Column(Text, nullable=True)
    challenges = Column(JSONB, default=list)
    completion_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserAccount", back_populates="business_identity")


# ── Conversations ──

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserAccount", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    agent_id = Column(String, nullable=True)
    token_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


# ── Content Pipeline ──

class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    content_type = Column(String, nullable=False)  # blog, social, email, ad, video_script
    platform = Column(String, nullable=True)       # linkedin, instagram, facebook, etc.
    title = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    media_urls = Column(JSONB, default=list)
    status = Column(String, default="draft")       # draft, pending_review, approved, published, rejected
    scheduled_for = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    performance_metrics = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserAccount", back_populates="content_items")


class ContentTemplate(Base):
    __tablename__ = "content_templates"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    platform = Column(String, nullable=True)
    template_data = Column(JSONB, default=dict)


# ── CRM / Leads ──

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    company = Column(String, nullable=True)
    source_platform = Column(String, nullable=True)
    source_content_id = Column(String, nullable=True)
    icp_score = Column(Float, default=0.0)
    engagement_level = Column(String, default="cold")  # cold, warm, hot
    pipeline_stage = Column(String, default="lead")     # lead, qualified, opportunity, customer
    profile_data = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserAccount", back_populates="contacts")
    interactions = relationship("Interaction", back_populates="contact", cascade="all, delete-orphan")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(String, primary_key=True, default=generate_uuid)
    contact_id = Column(String, ForeignKey("contacts.id"), nullable=False)
    type = Column(String, nullable=False)       # email, call, meeting, social
    channel = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    direction = Column(String, default="outbound")  # inbound, outbound
    created_at = Column(DateTime, default=datetime.utcnow)

    contact = relationship("Contact", back_populates="interactions")


class NurtureSequence(Base):
    __tablename__ = "nurture_sequences"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    trigger_type = Column(String, nullable=True)  # signup, engagement, abandoned
    steps = Column(JSONB, default=list)
    status = Column(String, default="draft")  # draft, active, paused, completed
    created_at = Column(DateTime, default=datetime.utcnow)


# ── Campaigns ──

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=True)         # content, email, ad, social
    status = Column(String, default="draft")
    config = Column(JSONB, default=dict)
    budget = Column(Float, nullable=True)
    performance = Column(JSONB, default=dict)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("UserAccount", back_populates="campaigns")


# ── Workflows ──

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    template_name = Column(String, nullable=True)
    mode = Column(String, default="prebuilt")  # prebuilt, ai, manual
    config = Column(JSONB, default=dict)
    estimated_tokens = Column(Integer, default=0)
    actual_tokens = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserAccount", back_populates="workflows")
    executions = relationship("WorkflowExecution", back_populates="workflow", cascade="all, delete-orphan")


class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id = Column(String, primary_key=True, default=generate_uuid)
    workflow_id = Column(String, ForeignKey("workflows.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="running")
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    results = Column(JSONB, default=dict)
    transparency_log = Column(JSONB, default=list)
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)

    workflow = relationship("Workflow", back_populates="executions")


# ── Goals ──

class Goal(Base):
    __tablename__ = "goals"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    target_metric = Column(String, nullable=True)
    current_value = Column(Float, default=0.0)
    target_value = Column(Float, default=0.0)
    status = Column(String, default="active")  # active, completed, paused
    process_recording = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("UserAccount", back_populates="goals")
    milestones = relationship("Milestone", back_populates="goal", cascade="all, delete-orphan")


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(String, primary_key=True, default=generate_uuid)
    goal_id = Column(String, ForeignKey("goals.id"), nullable=False)
    title = Column(String, nullable=False)
    reached_at = Column(DateTime, nullable=True)
    process_snapshot = Column(JSONB, default=dict)
    repeatable = Column(Boolean, default=False)

    goal = relationship("Goal", back_populates="milestones")


# ── Calendar ──

class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    source_platform = Column(String, nullable=True)  # google, outlook, guild
    category = Column(String, nullable=True)          # content, meeting, campaign, follow_up
    is_recurring = Column(Boolean, default=False)
    event_metadata = Column(JSONB, default=dict)

    user = relationship("UserAccount", back_populates="calendar_events")


class CalendarPattern(Base):
    __tablename__ = "calendar_patterns"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    pattern_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    confidence = Column(Float, default=0.0)
    learned_at = Column(DateTime, default=datetime.utcnow)


# ── Billing & Usage ──

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    plan = Column(String, default="free")  # free, starter, growth, scale
    status = Column(String, default="active")
    paystack_id = Column(String, nullable=True)
    token_budget = Column(Integer, default=100_000)
    tokens_used_month = Column(Integer, default=0)
    content_count_month = Column(Integer, default=0)
    video_count_month = Column(Integer, default=0)
    billing_cycle_start = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserAccount", back_populates="subscription")


class TokenUsage(Base):
    __tablename__ = "token_usage"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    agent_id = Column(String, nullable=True)
    workflow_id = Column(String, nullable=True)
    model = Column(String, nullable=False)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserAccount", back_populates="token_usage")


# ── Integrations ──

class ConnectedIntegration(Base):
    __tablename__ = "connected_integrations"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    platform = Column(String, nullable=False)
    status = Column(String, default="connected")
    oauth_tokens_encrypted = Column(JSONB, default=dict)
    last_synced = Column(DateTime, nullable=True)
    config = Column(JSONB, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserAccount", back_populates="connected_integrations")


# ── Knowledge Base ──

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=True)
    chunk_count = Column(Integer, default=0)
    embedded_at = Column(DateTime, nullable=True)
    doc_metadata = Column(JSONB, default=dict)

    user = relationship("UserAccount", back_populates="knowledge_documents")


# ── Agent Events (Theater) ──

class AgentEventRecord(Base):
    __tablename__ = "agent_event_records"

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, nullable=False, index=True)
    workflow_name = Column(String, nullable=True)
    event_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    how = Column(Text, nullable=True)
    why = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    data_json = Column(JSONB, default=dict)
    progress = Column(Float, default=0.0)


# ── CRM Expansion (Customer Journey) ──

class CustomerJourney(Base):
    __tablename__ = "customer_journeys"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    customer_email = Column(String, nullable=False, index=True)
    stage = Column(String, default="visitor")
    data = Column(JSONB, default=dict)
    health_score = Column(Float, default=50.0)
    conversion_probability = Column(Float, default=0.0)
    churn_risk = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



# ── Media Library ──

class MediaAsset(Base):
    __tablename__ = "media_assets"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # File info
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)          # image/jpeg, image/png, video/mp4
    file_size = Column(Integer, nullable=False)          # bytes
    storage_url = Column(String, nullable=False)         # full URL to retrieve the file
    thumbnail_url = Column(String, nullable=True)        # smaller version for grid display

    # AI-generated metadata
    ai_description = Column(Text, nullable=True)         # "A soy candle in a glass jar on wooden table"
    ai_tags = Column(JSONB, default=list)                # ["product", "candle", "spring"]
    ai_colors = Column(JSONB, default=list)              # ["#F5E6D3", "#8B4513", "#FFD700"]
    ai_embedding_id = Column(String, nullable=True)      # Qdrant point ID for semantic search

    # User metadata
    category = Column(String, nullable=True)             # "products", "team", "lifestyle", "logo", "brand"
    user_tags = Column(JSONB, default=list)
    alt_text = Column(String, nullable=True)             # accessibility text

    # Dimensions
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserAccount", back_populates="media_assets")


# ── Legacy compatibility aliases ──
LLMUsageRecord = TokenUsage
Project = Goal
ProjectMilestone = Milestone
AgentAuthorization = AgentEventRecord
AdaptiveLearningSignal = AgentEventRecord
AIActionOutcome = AgentEventRecord
UserPreference = AgentEventRecord
LearnedPattern = AgentEventRecord
AgentTrigger = AgentEventRecord
AgentOutput = AgentEventRecord
IntegrationCredential = ConnectedIntegration

