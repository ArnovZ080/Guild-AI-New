from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, List, Any, Optional
import os
import uuid
from datetime import datetime

from services.core.agents.identity import identity_manager
from services.core.agents.models import BusinessIdentity, KnowledgeSource
from services.core.logging import logger
from services.core.tools.document_processor import document_processor

router = APIRouter(prefix="/identity", tags=["identity"])

@router.get("/", response_model=BusinessIdentity)
async def get_identity():
    """Retrieve the current persistent business identity."""
    try:
        return identity_manager.get_identity()
    except Exception as e:
        logger.error(f"Failed to retrieve identity: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=BusinessIdentity)
async def update_identity(identity: BusinessIdentity):
    """Update or initialize the persistent business identity."""
    try:
        identity_manager.save(identity)
        return identity
    except Exception as e:
        logger.error(f"Failed to save identity: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/document", response_model=KnowledgeSource)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a business document to the knowledge base."""
    temp_path = None
    try:
        # 1. Save uploaded file to temp location
        os.makedirs("temp_uploads", exist_ok=True)
        temp_path = os.path.join("temp_uploads", f"{uuid.uuid4()}_{file.filename}")
        
        with open(temp_path, "wb") as f:
            f.write(await file.read())
            
        # 2. Process with DocumentProcessor
        result = document_processor.process_document(temp_path)
        
        if result["status"] == "failed":
            raise HTTPException(status_code=400, detail=result["error"])
            
        # 3. Create KnowledgeSource entry
        new_source = KnowledgeSource(
            id=str(uuid.uuid4()),
            type="file",
            name=file.filename,
            content_preview=result["content"][:500] + "...", # Store a preview
            indexed_at=datetime.now().isoformat()
        )
        
        # 4. Update Identity Knowledge Base
        identity = identity_manager.get_identity()
        identity.knowledge_base.append(new_source)
        identity_manager.save(identity)
        
        return new_source
        
    except Exception as e:
        logger.error(f"Failed to process document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
