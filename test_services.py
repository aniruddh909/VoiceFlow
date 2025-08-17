#!/usr/bin/env python3
"""
Test script to verify HuggingFace services are working correctly
"""
import asyncio
import os
import sys

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.hf_whisper_service import HuggingFaceWhisperService
from backend.services.hf_text_service import HuggingFaceTextService

async def test_services():
    print("Testing HuggingFace Services...")
    
    # Test text service
    print("\n1. Testing HuggingFace Text Service...")
    try:
        text_service = HuggingFaceTextService()
        test_text = "This is a test note that needs refinement."
        result = await text_service.refine_text(test_text, tone="casual")
        print(f"✅ Text service working! Result: {result}")
    except Exception as e:
        print(f"❌ Text service error: {e}")
    
    # Test whisper service (just initialization)
    print("\n2. Testing HuggingFace Whisper Service initialization...")
    try:
        whisper_service = HuggingFaceWhisperService()
        print("✅ Whisper service initialized successfully!")
    except Exception as e:
        print(f"❌ Whisper service error: {e}")
    
    print("\n🎉 Service tests completed!")

if __name__ == "__main__":
    asyncio.run(test_services())
