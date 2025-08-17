import openai
import os
from typing import Optional
import tempfile
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WhisperService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "sk-your-openai-api-key-here":
            raise Exception("OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.")
        
        # Set the API key for the v0.x library
        openai.api_key = api_key
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def transcribe(self, audio_file_path: str) -> str:
        """
        Transcribe audio file using OpenAI Whisper
        """
        try:
            print(f"Starting transcription of: {audio_file_path}")
            
            # Check if file exists and is readable
            if not os.path.exists(audio_file_path):
                raise Exception(f"Audio file not found: {audio_file_path}")
            
            file_size = os.path.getsize(audio_file_path)
            print(f"Audio file size: {file_size} bytes")
            
            if file_size == 0:
                raise Exception("Audio file is empty")
            
            # Run the transcription in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._transcribe_sync,
                audio_file_path
            )
            print(f"Transcription result length: {len(result)} characters")
            return result
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            raise Exception(f"Transcription failed: {str(e)}")
    
    def _transcribe_sync(self, audio_file_path: str) -> str:
        """
        Synchronous transcription method using v0.x API
        """
        try:
            print(f"Opening audio file: {audio_file_path}")
            with open(audio_file_path, "rb") as audio_file:
                print("Calling OpenAI Whisper API...")
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file
                )
                print(f"OpenAI API response received: {type(transcript)}")
                return transcript["text"]
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            raise e
    
    async def transcribe_with_timestamps(self, audio_file_path: str) -> dict:
        """
        Transcribe audio with timestamp information
        """
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._transcribe_with_timestamps_sync,
                audio_file_path
            )
            return result
        except Exception as e:
            raise Exception(f"Transcription with timestamps failed: {str(e)}")
    
    def _transcribe_with_timestamps_sync(self, audio_file_path: str) -> dict:
        """
        Synchronous transcription with timestamps using v0.x API
        """
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
        return transcript
    
    def validate_audio_file(self, file_path: str) -> bool:
        """
        Validate if the audio file is supported
        """
        supported_extensions = ['.mp3', '.wav', '.m4a', '.mp4', '.mpeg', '.mpga', '.webm']
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension in supported_extensions
