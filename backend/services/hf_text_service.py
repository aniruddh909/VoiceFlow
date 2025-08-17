import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceTextService:
    """Service for handling text refinement using Hugging Face models"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.executor = ThreadPoolExecutor(max_workers=2)
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the text generation model"""
        try:
            logger.info("Loading text generation model from Hugging Face...")
            
            # Get Hugging Face token if available
            self.hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
            
            # Detect device
            device = 0 if torch.cuda.is_available() else -1  # 0 for GPU, -1 for CPU
            
            # Use a smaller, efficient model for text refinement
            # Options: "microsoft/DialoGPT-medium", "gpt2", "distilgpt2"
            self.model_name = "microsoft/DialoGPT-medium"
            
            # Try to use a text generation pipeline (easier to use)
            self.pipeline = pipeline(
                "text-generation",
                model=self.model_name,
                tokenizer=self.model_name,
                device=device,
                token=self.hf_token,
                pad_token_id=50256,
                max_length=512,
                do_sample=True,
                temperature=0.7
            )
            
            logger.info(f"Text generation model loaded: {self.model_name}")
            if torch.cuda.is_available():
                logger.info("Model loaded on GPU")
            else:
                logger.info("Model loaded on CPU")
                logger.info("Model loaded on CPU")
                
        except Exception as e:
            logger.error(f"Failed to initialize text model: {str(e)}")
            # Fallback to a simpler approach
            self._initialize_fallback_model()
    
    def _initialize_fallback_model(self):
        """Initialize a smaller fallback model"""
        try:
            logger.info("Loading fallback model: distilgpt2")
            model_name = "distilgpt2"
            
            # Get Hugging Face token if available
            hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
            
            self.pipeline = pipeline(
                "text-generation",
                model=model_name,
                device=0 if torch.cuda.is_available() else -1,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                use_auth_token=hf_token if hf_token else None
            )
            logger.info("Fallback model loaded successfully")
        except Exception as e:
            logger.error(f"Fallback model failed: {str(e)}")
            raise Exception(f"Text model initialization failed: {str(e)}")
    
    # Tone-based prompts for text refinement
    tone_prompts = {
        "casual": {
            "system": "You are a helpful assistant that improves transcribed text while keeping it casual and conversational.",
            "instruction": "Please improve the following transcribed text by removing filler words, fixing grammar, and organizing it into clear paragraphs while maintaining a casual, conversational tone:"
        },
        
        "formal": {
            "system": "You are a professional writing assistant that transforms casual speech into formal, well-structured text.",
            "instruction": "Please transform the following transcribed text into formal, professional writing with proper grammar, structure, and tone:"
        },
        
        "like_me": {
            "system": "You are an assistant that cleans up transcribed text while preserving the speaker's unique voice and personality.",
            "instruction": "Please clean up the following transcribed text by removing filler words and fixing basic errors, but keep the speaker's natural style and personality intact:"
        }
    }
    
    async def refine_text(
        self, 
        text: str, 
        tone: str = "casual", 
        custom_prompt: Optional[str] = None
    ) -> str:
        """
        Refine text using Hugging Face models
        """
        try:
            if not self.pipeline:
                self._initialize_model()
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._refine_text_sync,
                text,
                tone,
                custom_prompt
            )
            return result
        except Exception as e:
            logger.error(f"Text refinement failed: {str(e)}")
            raise Exception(f"Text refinement failed: {str(e)}")
    
    def _refine_text_sync(self, text: str, tone: str, custom_prompt: Optional[str]) -> str:
        """
        Synchronous text refinement
        """
        try:
            # Get the appropriate prompt
            prompt_info = self.tone_prompts.get(tone, self.tone_prompts["casual"])
            
            if custom_prompt:
                instruction = custom_prompt
            else:
                instruction = prompt_info["instruction"]
            
            # Create the full prompt
            full_prompt = f"{instruction}\n\nOriginal text: \"{text}\"\n\nImproved text:"
            
            # Generate improved text
            response = self.pipeline(
                full_prompt,
                max_length=len(full_prompt.split()) + 200,  # Allow for expansion
                min_length=len(full_prompt.split()) + 20,   # Minimum expansion
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.pipeline.tokenizer.eos_token_id,
                num_return_sequences=1,
                truncation=True
            )
            
            # Extract the generated text
            generated_text = response[0]['generated_text']
            
            # Try to extract just the improved text part
            if "Improved text:" in generated_text:
                improved_text = generated_text.split("Improved text:")[-1].strip()
            else:
                # Fallback: take the part after the original prompt
                improved_text = generated_text[len(full_prompt):].strip()
            
            # Clean up the result
            improved_text = self._clean_generated_text(improved_text)
            
            # If the result is too short or doesn't look good, provide a fallback
            if len(improved_text) < 10 or not improved_text:
                improved_text = self._fallback_refinement(text, tone)
            
            logger.info(f"Text refined: {len(text)} -> {len(improved_text)} characters")
            return improved_text
            
        except Exception as e:
            logger.error(f"Sync text refinement failed: {str(e)}")
            # Provide fallback refinement
            return self._fallback_refinement(text, tone)
    
    def _clean_generated_text(self, text: str) -> str:
        """Clean up generated text"""
        # Remove common generation artifacts
        text = text.replace("<|endoftext|>", "")
        text = text.replace("</s>", "")
        text = text.replace("<s>", "")
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Remove incomplete sentences at the end
        sentences = text.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
            text = '.'.join(sentences[:-1]) + '.'
        
        return text.strip()
    
    def _fallback_refinement(self, text: str, tone: str) -> str:
        """Simple fallback text refinement without AI"""
        try:
            # Basic text cleaning
            import re
            
            # Remove common filler words
            filler_words = ['um', 'uh', 'like', 'you know', 'so', 'well']
            for filler in filler_words:
                text = re.sub(r'\b' + filler + r'\b', '', text, flags=re.IGNORECASE)
            
            # Clean up extra spaces
            text = re.sub(r'\s+', ' ', text)
            
            # Capitalize first letter and add period if missing
            text = text.strip()
            if text:
                text = text[0].upper() + text[1:]
                if not text.endswith(('.', '!', '?')):
                    text += '.'
            
            return text if text else "I apologize, but I couldn't process the audio properly. Please try again."
            
        except Exception as e:
            logger.error(f"Fallback refinement failed: {str(e)}")
            return "I apologize, but I couldn't process the audio properly. Please try again."
    
    async def generate_summary(self, text: str) -> str:
        """
        Generate a brief summary of the text
        """
        try:
            # For now, provide a simple extractive summary
            sentences = text.split('.')
            if len(sentences) <= 2:
                return text
            
            # Take first and last sentences as a simple summary
            summary = f"{sentences[0].strip()}. {sentences[-2].strip()}."
            return summary
            
        except Exception as e:
            logger.error(f"Summary generation failed: {str(e)}")
            return "Summary could not be generated."
    
    async def analyze_tone(self, text: str) -> dict:
        """
        Analyze the tone and style of the text
        """
        try:
            # Simple tone analysis based on text characteristics
            word_count = len(text.split())
            
            # Basic sentiment indicators
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing']
            
            positive_count = sum(1 for word in positive_words if word in text.lower())
            negative_count = sum(1 for word in negative_words if word in text.lower())
            
            if positive_count > negative_count:
                sentiment = "positive"
            elif negative_count > positive_count:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            analysis = f"This text appears to have a {sentiment} tone with approximately {word_count} words."
            
            return {"analysis": analysis}
            
        except Exception as e:
            logger.error(f"Tone analysis failed: {str(e)}")
            return {"analysis": "Tone analysis could not be completed."}
