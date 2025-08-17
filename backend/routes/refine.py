from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..services.hf_text_service import HuggingFaceTextService
from ..services.db import DatabaseService
from typing import Optional

router = APIRouter()

# Initialize services lazily
def get_gpt_service():
    return HuggingFaceTextService()

def get_db_service():
    return DatabaseService()

class RefineRequest(BaseModel):
    note_id: str
    tone: str = "casual"  # casual, formal, like_me
    custom_prompt: Optional[str] = None

class CustomPromptRequest(BaseModel):
    prompt: str
    save_as_default: bool = False

@router.post("/improve")
async def refine_text(request: RefineRequest):
    """
    Refine transcribed text using GPT for better structure and clarity
    """
    try:
        # Get original transcript
        db_service = get_db_service()
        note = await db_service.get_note(request.note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        # Refine text using GPT
        gpt_service = get_gpt_service()
        refined_text = await gpt_service.refine_text(
            text=note.original_text,
            tone=request.tone,
            custom_prompt=request.custom_prompt
        )
        
        # Update note with refined text
        await db_service.update_note(request.note_id, refined_text=refined_text)
        
        return JSONResponse(content={
            "success": True,
            "note_id": request.note_id,
            "original_text": note.original_text,
            "refined_text": refined_text,
            "tone": request.tone
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/custom-prompt")
async def save_custom_prompt(request: CustomPromptRequest):
    """
    Save or update user's custom prompt for text refinement
    """
    try:
        if request.save_as_default:
            db_service = get_db_service()
            await db_service.save_user_prompt(request.prompt)
        
        return JSONResponse(content={
            "success": True,
            "prompt": request.prompt,
            "saved_as_default": request.save_as_default
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tones")
async def get_available_tones():
    """
    Get list of available tone options
    """
    return JSONResponse(content={
        "tones": [
            {"id": "casual", "name": "Casual", "description": "Relaxed and conversational"},
            {"id": "formal", "name": "Formal", "description": "Professional and structured"},
            {"id": "like_me", "name": "Like Me", "description": "Maintains your personal style"}
        ]
    })
