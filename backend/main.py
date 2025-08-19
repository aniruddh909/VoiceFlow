from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes after loading env vars
from .routes import transcribe, refine, notes

app = FastAPI(
    title="VoiceFlow AI",
    description="Audio-to-text transcription with AI-powered refinement",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving removed - using Vite dev server for frontend in development
# In production, you would build the React app and serve static files here

# Include routers
app.include_router(transcribe.router, prefix="/api/transcribe", tags=["transcribe"])
app.include_router(refine.router, prefix="/api/refine", tags=["refine"])
app.include_router(notes.router, prefix="/api/notes", tags=["notes"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main:app", 
        host=host, 
        port=port, 
        reload=debug,
        reload_dirs=[".", "../frontend"] if debug else None
    )
