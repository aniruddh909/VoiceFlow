#!/usr/bin/env python3
"""
Start script for VoiceFlow AI server
"""
import uvicorn
import os

if __name__ == "__main__":
    # Change to the project directory
    os.chdir("/Users/aniruddh/Documents/VoiceFlow")
    
    # Start the server
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
