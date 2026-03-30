import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from services.core.db.base import AsyncSessionLocal
from services.core.db.models import CustomerJourney as DBCustomerJourney
from .models import (
    JourneyStage, TouchpointType, Touchpoint, Milestone,
    CustomerJourney as PydanticCustomerJourney
)

logger = logging.getLogger(__name__)

# --- Stage Configuration (replaces 150 lines of legacy init code) ---

STAGE_PROGRESSION = {
    JourneyStage.AWARENESS:     [JourneyStage.CONSIDERATION],
    JourneyStage.CONSIDERATION: [JourneyStage.PURCHASE, JourneyStage.AWARENESS],
    JourneyStage.PURCHASE:      [JourneyStage.ONBOARDING],
    JourneyStage.ONBOARDING:    [JourneyStage.ADOPTION],
    JourneyStage.ADOPTION:      [JourneyStage.RETENTION, JourneyStage.CHURN],
    JourneyStage.RETENTION:     [JourneyStage.ADVOCACY, JourneyStage.CHURN],
    JourneyStage.ADVOCACY:      [JourneyStage.RETENTION, JourneyStage.CHURN],
    JourneyStage.CHURN:         [],
}

TOUCHPOINT_SCORES = {
    TouchpointType.WEBSITE_VISIT:      1.0,
    TouchpointType.EMAIL_OPEN:         2.0,
    TouchpointType.EMAIL_CLICK:        3.0,
    TouchpointType.SOCIAL_ENGAGEMENT:  2.5,
    TouchpointType.SUPPORT_TICKET:     4.0,
    TouchpointType.PHONE_CALL:         5.0,
    TouchpointType.MEETING:            6.0,
    TouchpointType.DEMO:               8.0,
    TouchpointType.TRIAL_START:        7.0,
    TouchpointType.PURCHASE:          10.0,
    TouchpointType.UPGRADE:            8.0,
    TouchpointType.FEEDBACK:           3.0,
    TouchpointType.REFERRAL:           9.0,
}

TOUCHPOINT_STAGE_MAP = {
    TouchpointType.WEBSITE_VISIT:      JourneyStage.AWARENESS,
    TouchpointType.EMAIL_OPEN:         JourneyStage.CONSIDERATION,
    TouchpointType.EMAIL_CLICK:        JourneyStage.CONSIDERATION,
    TouchpointType.SOCIAL_ENGAGEMENT:  JourneyStage.AWARENESS,
    TouchpointType.SUPPORT_TICKET:     JourneyStage.ADOPTION,
    TouchpointType.PHONE_CALL:         JourneyStage.CONSIDERATION,
    TouchpointType.MEETING:            JourneyStage.CONSIDERATION,
    TouchpointType.DEMO:               JourneyStage.CONSIDERATION,
    TouchpointType.TRIAL_START:        JourneyStage.CONSIDERATION,
    TouchpointType.PURCHASE:           JourneyStage.PURCHASE,
    TouchpointType.UPGRADE:            JourneyStage.RETENTION,
    TouchpointType.FEEDBACK:           JourneyStage.ADOPTION,
    TouchpointType.REFERRAL:           JourneyStage.ADVOCACY,
}

# Milestone triggers: touchpoint type -> milestone event name
MILESTONE_TRIGGERS = {
    TouchpointType.WEBSITE_VISIT:      "first_contact",
    TouchpointType.EMAIL_CLICK:        "first_engagement",
    TouchpointType.TRIAL_START:        "trial_start",
    TouchpointType.PURCHASE:           "first_purchase",
    TouchpointType.UPGRADE:            "first_upgrade",
    TouchpointType.REFERRAL:           "first_referral",
}

class JourneyTracker:
    """
    Manages customer journeys with automatic stage progression,
    churn risk scoring, and milestone detection using PostgreSQL.
    """

    # --- Touchpoint Recording ---

    @classmethod
    async def track(cls, db: Optional[AsyncSession], user_id: str, customer_email: str, touchpoint_type: TouchpointType,
              channel: str, platform: str, **kwargs) -> Touchpoint:
        """
        Record a customer touchpoint and update their journey.
        """
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            journey, db_journey = await cls._get_or_create(db, user_id, customer_email)
            
            tp = Touchpoint(
                customer_id=customer_email,
                type=touchpoint_type,
                channel=channel,
                platform=platform,
                stage=TOUCHPOINT_STAGE_MAP.get(touchpoint_type, JourneyStage.AWARENESS),
                sentiment=kwargs.get("sentiment"),
                outcome=kwargs.get("outcome"),
                value=kwargs.get("value"),
                metadata=kwargs.get("metadata", {}),
            )
            
            journey.touchpoints.append(tp)
            journey.last_activity = tp.timestamp
            
            cls._try_advance_stage(journey, tp)
            cls._check_milestones(journey, tp)
            cls._recalculate_metrics(journey)
            
            # Save back to db
            db_journey.status = journey.current_stage.value
            db_journey.data = journey.model_dump(mode="json")
            await db.commit()
            
            logger.info(f"JourneyTracker: [{customer_email}] {touchpoint_type.value} → stage={journey.current_stage.value}, health={journey.health}")
            return tp
        finally:
            if should_close:
                await db.close()

    # --- Query ---

    @classmethod
    async def get_journey(cls, db: Optional[AsyncSession], user_id: str, customer_email: str) -> Optional[PydanticCustomerJourney]:
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            stmt = select(DBCustomerJourney).where(
                DBCustomerJourney.user_id == user_id,
                DBCustomerJourney.customer_email == customer_email
            )
            result = await db.execute(stmt)
            db_journey = result.scalar_one_or_none()
            if not db_journey or not db_journey.data:
                return None
            return PydanticCustomerJourney(**db_journey.data)
        finally:
            if should_close:
                await db.close()

    @classmethod
    async def get_all_journeys(cls, db: Optional[AsyncSession], user_id: str) -> List[PydanticCustomerJourney]:
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            stmt = select(DBCustomerJourney).where(DBCustomerJourney.user_id == user_id)
            result = await db.execute(stmt)
            db_journeys = result.scalars().all()
            return [PydanticCustomerJourney(**j.data) for j in db_journeys if j.data]
        finally:
            if should_close:
                await db.close()

    @classmethod
    async def get_at_risk_customers(cls, db: Optional[AsyncSession], user_id: str) -> List[PydanticCustomerJourney]:
        """Return customers with churn_risk > 0.5, sorted by risk."""
        journeys = await cls.get_all_journeys(db, user_id)
        return sorted(
            [j for j in journeys if j.churn_risk > 0.5],
            key=lambda j: j.churn_risk,
            reverse=True
        )

    @classmethod
    async def get_analytics(cls, db: Optional[AsyncSession], user_id: str) -> Dict[str, Any]:
        """Aggregated funnel analytics."""
        journeys = await cls.get_all_journeys(db, user_id)
        if not journeys:
            return {"total_customers": 0}

        stage_counts = {}
        for stage in JourneyStage:
            stage_counts[stage.value] = sum(1 for j in journeys if j.current_stage == stage)

        health_counts = {"excellent": 0, "good": 0, "warning": 0, "critical": 0}
        for j in journeys:
            health_counts[j.health] = health_counts.get(j.health, 0) + 1

        return {
            "total_customers": len(journeys),
            "stage_distribution": stage_counts,
            "health_distribution": health_counts,
            "avg_journey_score": sum(j.journey_score for j in journeys) / len(journeys),
            "avg_churn_risk": sum(j.churn_risk for j in journeys) / len(journeys),
            "at_risk_count": sum(1 for j in journeys if j.churn_risk > 0.5),
        }

    # --- Internal Logic ---

    @classmethod
    async def _get_or_create(cls, db: AsyncSession, user_id: str, customer_email: str) -> tuple[PydanticCustomerJourney, DBCustomerJourney]:
        stmt = select(DBCustomerJourney).where(
            DBCustomerJourney.user_id == user_id,
            DBCustomerJourney.customer_email == customer_email
        )
        result = await db.execute(stmt)
        db_journey = result.scalar_one_or_none()
        
        if db_journey is None:
            # Create new
            db_journey = DBCustomerJourney(
                user_id=user_id,
                customer_email=customer_email,
                segment="default",
                status="active",
                data={}
            )
            db.add(db_journey)
            # Default empty journey data
            journey = PydanticCustomerJourney(customer_id=customer_email)
            db_journey.data = journey.model_dump(mode="json")
            await db.flush()
            return journey, db_journey
        else:
            if not db_journey.data:
                journey = PydanticCustomerJourney(customer_id=customer_email)
            else:
                journey = PydanticCustomerJourney(**db_journey.data)
            return journey, db_journey

    @classmethod
    def _try_advance_stage(cls, journey: PydanticCustomerJourney, tp: Touchpoint):
        """Advance the stage if the touchpoint implies a valid progression."""
        tp_stage = tp.stage
        valid_next = STAGE_PROGRESSION.get(journey.current_stage, [])
        if tp_stage in valid_next:
            journey.current_stage = tp_stage
            journey.days_in_stage = 0

    @classmethod
    def _check_milestones(cls, journey: PydanticCustomerJourney, tp: Touchpoint):
        """Check if this touchpoint triggers a milestone (only once per type)."""
        event_name = MILESTONE_TRIGGERS.get(tp.type)
        if not event_name:
            return
        already_exists = any(m.event == event_name for m in journey.milestones)
        if not already_exists:
            journey.milestones.append(Milestone(
                customer_id=journey.customer_id,
                event=event_name,
                stage=journey.current_stage,
                impact_score=TOUCHPOINT_SCORES.get(tp.type, 1.0),
                description=f"Customer reached: {event_name.replace('_', ' ').title()}"
            ))

    @classmethod
    def _recalculate_metrics(cls, journey: PydanticCustomerJourney):
        """Recalculate journey score, churn risk, health, and predictions."""
        # Journey score: sum of touchpoint scores, capped at 100
        total = sum(TOUCHPOINT_SCORES.get(tp.type, 1.0) for tp in journey.touchpoints)
        journey.journey_score = min(100.0, total)

        # Duration
        from datetime import timezone
        now = datetime.now(timezone.utc)
        
        # Ensure timezone-aware subtraction
        j_start = journey.journey_start
        if j_start.tzinfo is None:
            j_start = j_start.replace(tzinfo=timezone.utc)
            
        j_last = journey.last_activity
        if j_last.tzinfo is None:
            j_last = j_last.replace(tzinfo=timezone.utc)
            
        journey.total_duration_days = (j_last - j_start).days

        # Churn risk
        journey.churn_risk = cls._compute_churn_risk(journey)

        # Next stage prediction
        journey.next_likely_stage = cls._predict_next_stage(journey)

        # Health
        journey.health = cls._compute_health(journey)

        # Conversion probability
        journey.conversion_probability = cls._compute_conversion(journey)

    @classmethod
    def _compute_churn_risk(cls, journey: PydanticCustomerJourney) -> float:
        risk = 0.0
        from datetime import timezone
        now = datetime.now(timezone.utc)
        
        j_last = journey.last_activity
        if j_last.tzinfo is None:
            j_last = j_last.replace(tzinfo=timezone.utc)

        # Inactivity risk
        days_inactive = (now - j_last).days
        if days_inactive > 30:
            risk += 0.4
        elif days_inactive > 14:
            risk += 0.2

        # Stuck in stage risk
        if journey.current_stage in [JourneyStage.ADOPTION, JourneyStage.RETENTION]:
            if journey.days_in_stage > 90:
                risk += 0.3

        # Stuck in early stages
        if journey.current_stage in [JourneyStage.AWARENESS, JourneyStage.CONSIDERATION]:
            if journey.total_duration_days > 30:
                risk += 0.3

        # Support overload
        support_count = sum(1 for tp in journey.touchpoints if tp.type == TouchpointType.SUPPORT_TICKET)
        if support_count > 3:
            risk += 0.2

        return min(1.0, risk)

    @classmethod
    def _predict_next_stage(cls, journey: PydanticCustomerJourney) -> Optional[JourneyStage]:
        s = journey.journey_score
        stage = journey.current_stage
        if stage == JourneyStage.AWARENESS and s > 20:
            return JourneyStage.CONSIDERATION
        elif stage == JourneyStage.CONSIDERATION and s > 40:
            return JourneyStage.PURCHASE
        elif stage == JourneyStage.PURCHASE:
            return JourneyStage.ONBOARDING
        elif stage == JourneyStage.ONBOARDING and s > 60:
            return JourneyStage.ADOPTION
        elif stage == JourneyStage.ADOPTION:
            if journey.churn_risk > 0.7:
                return JourneyStage.CHURN
            elif s > 80:
                return JourneyStage.RETENTION
        elif stage == JourneyStage.RETENTION:
            if journey.churn_risk > 0.6:
                return JourneyStage.CHURN
            elif s > 90:
                return JourneyStage.ADVOCACY
        return None

    @classmethod
    def _compute_health(cls, journey: PydanticCustomerJourney) -> str:
        if journey.churn_risk > 0.7:
            return "critical"
        elif journey.churn_risk > 0.4:
            return "warning"
        elif journey.journey_score > 70 and journey.conversion_probability > 0.5:
            return "excellent"
        elif journey.journey_score > 40:
            return "good"
        return "warning"

    @classmethod
    def _compute_conversion(cls, journey: PydanticCustomerJourney) -> float:
        stage_rates = {
            JourneyStage.AWARENESS: 0.15,
            JourneyStage.CONSIDERATION: 0.25,
            JourneyStage.PURCHASE: 1.0,
            JourneyStage.ONBOARDING: 0.8,
            JourneyStage.ADOPTION: 0.7,
            JourneyStage.RETENTION: 0.6,
            JourneyStage.ADVOCACY: 0.3,
            JourneyStage.CHURN: 0.0,
        }
        base = stage_rates.get(journey.current_stage, 0.0)
        activity_factor = min(1.0, len(journey.touchpoints) / 10.0)
        score_factor = journey.journey_score / 100.0
        return base * activity_factor * score_factor
