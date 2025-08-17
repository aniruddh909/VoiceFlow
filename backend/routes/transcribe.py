from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ..services.hf_whisper_service import HuggingFaceWhisperService
from ..services.db import DatabaseService
import tempfile
import os
from datetime import datetime

router = APIRouter()

# Initialize services lazily
def get_whisper_service():
    return HuggingFaceWhisperService()

def get_db_service():
    return DatabaseService()

@router.post("/upload")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Upload and transcribe audio file using OpenAI Whisper
    """
    try:
        print(f"Received file: {file.filename}, content_type: {file.content_type}")
        
        # Validate file type
        allowed_types = ["audio/mpeg", "audio/wav", "audio/mp4", "audio/x-m4a", "audio/webm"]
        if file.content_type not in allowed_types:
            print(f"Unsupported file type: {file.content_type}")
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file.content_type}. Please upload MP3, WAV, M4A, or WebM files."
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            content = await file.read()
            print(f"File size: {len(content)} bytes")
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            print(f"Starting transcription for: {tmp_file_path}")
            # Transcribe audio
            whisper_service = get_whisper_service()
            transcript = await whisper_service.transcribe(tmp_file_path)
            print(f"Transcription completed: {len(transcript)} characters")
            
            # Save to database
            db_service = get_db_service()
            note_id = await db_service.save_note(
                original_text=transcript,
                filename=file.filename,
                created_at=datetime.utcnow()
            )
            print(f"Note saved with ID: {note_id}")
            
            return JSONResponse(content={
                "success": True,
                "note_id": note_id,
                "transcript": transcript,
                "filename": file.filename
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
                print(f"Cleaned up temp file: {tmp_file_path}")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@router.get("/status/{note_id}")
async def get_transcription_status(note_id: str):
    """
    Get the status of a transcription job
    """
    try:
        db_service = get_db_service()
        note = await db_service.get_note(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        return JSONResponse(content={
            "note_id": note_id,
            "status": "completed",
            "transcript": note.original_text
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
