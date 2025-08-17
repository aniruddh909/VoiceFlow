import openai
import os
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GPTService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "sk-your-openai-api-key-here":
            raise Exception("OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.")
        
        # Use v0.x API approach
        openai.api_key = api_key
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Default prompts for different tones
        self.tone_prompts = {
            "casual": """
            Please improve the following transcribed text by:
            1. Removing filler words (um, uh, like, you know)
            2. Fixing grammar and punctuation
            3. Organizing thoughts into clear paragraphs
            4. Maintaining a casual, conversational tone
            5. Keeping the original meaning and personal voice intact
            
            Keep it natural and conversational. Don't make it overly formal.
            """,
            
            "formal": """
            Please improve the following transcribed text by:
            1. Removing filler words and casual speech patterns
            2. Correcting grammar and punctuation
            3. Structuring content with clear paragraphs and logical flow
            4. Using professional language and tone
            5. Maintaining the original meaning while elevating the style
            
            Make it suitable for professional or academic contexts.
            """,
            
            "like_me": """
            Please improve the following transcribed text by:
            1. Removing only filler words and obvious speech errors
            2. Fixing basic grammar and punctuation
            3. Organizing into paragraphs while keeping the original style
            4. Preserving the speaker's unique voice and personality
            5. Maintaining all personal expressions and speaking patterns
            
            Keep the speaker's natural style and personality intact.
            """
        }
    
    async def refine_text(
        self, 
        text: str, 
        tone: str = "casual", 
        custom_prompt: Optional[str] = None
    ) -> str:
        """
        Refine text using GPT-4 for better structure and clarity
        """
        try:
            # Use custom prompt if provided, otherwise use tone-based prompt
            system_prompt = custom_prompt if custom_prompt else self.tone_prompts.get(tone, self.tone_prompts["casual"])
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._refine_text_sync,
                system_prompt,
                text
            )
            return result
        except Exception as e:
            raise Exception(f"Text refinement failed: {str(e)}")
    
    def _refine_text_sync(self, system_prompt: str, text: str) -> str:
        """
        Synchronous text refinement using v0.x API
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please improve this text:\n\n{text}"}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    
    async def generate_summary(self, text: str) -> str:
        """
        Generate a brief summary of the text
        """
        try:
            system_prompt = """
            Create a brief, clear summary of the following text. 
            Focus on the main points and key information.
            Keep it concise but comprehensive.
            """
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._generate_summary_sync,
                system_prompt,
                text
            )
            return result
        except Exception as e:
            raise Exception(f"Summary generation failed: {str(e)}")
    
    def _generate_summary_sync(self, system_prompt: str, text: str) -> str:
        """
        Synchronous summary generation using v0.x API
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    
    async def analyze_tone(self, text: str) -> dict:
        """
        Analyze the tone and style of the text
        """
        try:
            system_prompt = """
            Analyze the tone and style of the following text.
            Return your analysis in this format:
            - Tone: [describe the overall tone]
            - Formality: [formal/casual/mixed]
            - Key characteristics: [list 2-3 main style characteristics]
            """
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._analyze_tone_sync,
                system_prompt,
                text
            )
            return {"analysis": result}
        except Exception as e:
            raise Exception(f"Tone analysis failed: {str(e)}")
    
    def _analyze_tone_sync(self, system_prompt: str, text: str) -> str:
        """
        Synchronous tone analysis using v0.x API
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
