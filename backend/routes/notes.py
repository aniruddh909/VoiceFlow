from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from ..services.db import DatabaseService
from typing import Optional
import json

router = APIRouter()

# Initialize services lazily
def get_db_service():
    return DatabaseService()

@router.get("/")
async def get_notes(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    """
    Get user's note history with pagination
    """
    try:
        db_service = get_db_service()
        notes = await db_service.get_notes(limit=limit, offset=offset)
        total_count = await db_service.get_notes_count()
        
        return JSONResponse(content={
            "notes": [
                {
                    "id": note.id,
                    "filename": note.filename,
                    "original_text": note.original_text[:200] + "..." if len(note.original_text) > 200 else note.original_text,
                    "refined_text": note.refined_text[:200] + "..." if note.refined_text and len(note.refined_text) > 200 else note.refined_text,
                    "created_at": note.created_at.isoformat(),
                    "updated_at": note.updated_at.isoformat() if note.updated_at else None
                }
                for note in notes
            ],
            "total": total_count,
            "limit": limit,
            "offset": offset
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{note_id}")
async def get_note(note_id: str):
    """
    Get a specific note by ID
    """
    try:
        db_service = get_db_service()
        note = await db_service.get_note(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        return JSONResponse(content={
            "id": note.id,
            "filename": note.filename,
            "original_text": note.original_text,
            "refined_text": note.refined_text,
            "created_at": note.created_at.isoformat(),
            "updated_at": note.updated_at.isoformat() if note.updated_at else None
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{note_id}")
async def delete_note(note_id: str):
    """
    Delete a specific note
    """
    try:
        db_service = get_db_service()
        success = await db_service.delete_note(note_id)
        if not success:
            raise HTTPException(status_code=404, detail="Note not found")
        
        return JSONResponse(content={
            "success": True,
            "message": "Note deleted successfully"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{note_id}/export")
async def export_note(note_id: str, format: str = Query(default="txt")):
    """
    Export a note in different formats
    """
    try:
        db_service = get_db_service()
        note = await db_service.get_note(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        if format == "txt":
            content = note.refined_text or note.original_text
            return JSONResponse(content={
                "format": "txt",
                "content": content,
                "filename": f"{note.filename.split('.')[0]}.txt"
            })
        elif format == "json":
            content = {
                "original_text": note.original_text,
                "refined_text": note.refined_text,
                "filename": note.filename,
                "created_at": note.created_at.isoformat()
            }
            return JSONResponse(content={
                "format": "json",
                "content": json.dumps(content, indent=2),
                "filename": f"{note.filename.split('.')[0]}.json"
            })
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
