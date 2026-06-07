from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Dict, Any

from services.core.db.base import get_db
from services.core.db.models import UserAccount, Conversation, Message
from services.api.middleware.auth import get_current_user
from services.core.logging import logger

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/")
async def list_conversations(
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    """Get all conversations for the current user."""
    try:
        stmt = select(Conversation).where(Conversation.user_id == current_user.id).order_by(Conversation.updated_at.desc())
        result = await db.execute(stmt)
        conversations = result.scalars().all()
        return [
            {
                "id": c.id,
                "title": c.title,
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat()
            } for c in conversations
        ]
    except Exception as e:
        logger.error(f"Failed to list conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    """Get a specific conversation and its messages."""
    try:
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        ).options(selectinload(Conversation.messages))
        result = await db.execute(stmt)
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
            
        messages = sorted(conversation.messages, key=lambda m: m.created_at)
        return {
            "id": conversation.id,
            "title": conversation.title,
            "messages": [
                {
                    "id": m.id,
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.created_at.isoformat()
                } for m in messages
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{conversation_id}/message")
async def save_message(
    conversation_id: str,
    message_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    """Save a new message to a conversation."""
    try:
        # Check if conversation exists, if not, create it
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        result = await db.execute(stmt)
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            # Create new conversation
            title = message_data.get("content", "New Chat")[:50]
            conversation = Conversation(
                id=conversation_id,
                user_id=current_user.id,
                title=title
            )
            db.add(conversation)
            
        # Add message
        new_msg = Message(
            conversation_id=conversation.id,
            role=message_data.get("role", "user"),
            content=message_data.get("content", ""),
            token_count=message_data.get("tokens", 0)
        )
        db.add(new_msg)
        await db.commit()
        
        return {"status": "success", "message_id": new_msg.id}
    except Exception as e:
        logger.error(f"Failed to save message: {e}")
        raise HTTPException(status_code=500, detail=str(e))
