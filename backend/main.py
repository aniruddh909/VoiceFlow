from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Mount static files for frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

# Mount individual asset directories if they exist
js_path = os.path.join(frontend_path, "js")
css_path = os.path.join(frontend_path, "css")

if os.path.exists(js_path):
    app.mount("/js", StaticFiles(directory=js_path), name="js")
if os.path.exists(css_path):
    app.mount("/css", StaticFiles(directory=css_path), name="css")

# Mount the main static directory
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Include routers
app.include_router(transcribe.router, prefix="/api/transcribe", tags=["transcribe"])
app.include_router(refine.router, prefix="/api/refine", tags=["refine"])
app.include_router(notes.router, prefix="/api/notes", tags=["notes"])

@app.get("/")
async def root():
    """Serve the main frontend page"""
    return FileResponse(os.path.join(frontend_path, "index.html"))

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
