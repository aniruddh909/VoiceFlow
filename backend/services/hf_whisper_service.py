import os
import torch
import librosa
import numpy as np
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import asyncio
from concurrent.futures import ThreadPoolExecutor
import tempfile
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceWhisperService:
    """Service for handling audio transcription using Hugging Face Whisper"""
    
    def __init__(self):
        self.model = None
        self.processor = None
        self.executor = ThreadPoolExecutor(max_workers=2)
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Whisper model and processor lazily"""
        try:
            logger.info("Loading Whisper model from Hugging Face...")
            
            # Get Hugging Face token if available
            self.hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
            
            # Use Whisper base model
            self.model_name = "openai/whisper-base"
            
            # Load the processor and model with authentication token
            self.processor = WhisperProcessor.from_pretrained(
                self.model_name,
                token=self.hf_token
            )
            self.model = WhisperForConditionalGeneration.from_pretrained(
                self.model_name,
                token=self.hf_token
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                self.model = self.model.cuda()
                logger.info("Model loaded on GPU")
            else:
                logger.info("Model loaded on CPU")
                
        except Exception as e:
            logger.error(f"Failed to initialize Whisper model: {str(e)}")
            raise Exception(f"Whisper model initialization failed: {str(e)}")

    async def transcribe(self, audio_file_path: str) -> str:
        """
        Main transcribe method - matches the interface expected by routes
        """
        return await self.transcribe_audio(audio_file_path)

    async def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to text
        """
        try:
            if not self.model or not self.processor:
                self._initialize_model()
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._transcribe_sync,
                audio_file_path
            )
            return result
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise Exception(f"Transcription failed: {str(e)}")
    
    def _transcribe_sync(self, audio_file_path: str) -> str:
        """
        Synchronous transcription using Hugging Face Whisper
        """
        try:
            # Load audio using librosa (handles more formats)
            audio_input, sample_rate = librosa.load(audio_file_path, sr=16000, mono=True)
            
            # Ensure audio is the right shape
            if len(audio_input.shape) > 1:
                audio_input = audio_input.mean(axis=0)
            
            # Process with Whisper
            input_features = self.processor(
                audio_input, 
                sampling_rate=16000, 
                return_tensors="pt"
            ).input_features
            
            # Move to same device as model
            if torch.cuda.is_available() and self.model.device.type == 'cuda':
                input_features = input_features.cuda()
            
            # Generate transcription
            with torch.no_grad():
                predicted_ids = self.model.generate(input_features)
            
            # Decode the transcription
            transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            
            logger.info(f"Transcription completed: {len(transcription)} characters")
            return transcription.strip()
            
        except Exception as e:
            logger.error(f"Sync transcription failed: {str(e)}")
            raise Exception(f"Transcription processing failed: {str(e)}")
    
    async def transcribe_with_timestamps(self, audio_file_path: str) -> dict:
        """
        Transcribe audio with word-level timestamps (simplified version)
        """
        try:
            # For now, just return the basic transcription
            # Word-level timestamps require more complex implementation
            text = await self.transcribe_audio(audio_file_path)
            
            return {
                "text": text,
                "segments": [
                    {
                        "start": 0.0,
                        "end": 10.0,  # Placeholder
                        "text": text
                    }
                ]
            }
        except Exception as e:
            raise Exception(f"Timestamp transcription failed: {str(e)}")
