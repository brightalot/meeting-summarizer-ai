from openai import AsyncOpenAI
from app.core.config import settings
import os

class STTService:
    def __init__(self):
        # Ensure API key is present
        if settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            print("Warning: OPENAI_API_KEY is not set.")
            self.client = None

    async def transcribe(self, file_path: str) -> str:
        if not self.client:
            raise ValueError("OpenAI API Key is not configured.")
            
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(file_path, "rb") as audio_file:
            # Using Whisper-1 model
            transcript = await self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text

stt_service = STTService()

