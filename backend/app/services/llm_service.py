from google import genai
from app.core.config import settings

class LLMService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            # Initialize the client from google-genai SDK
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        else:
            print("Warning: GEMINI_API_KEY is not set.")
            self.client = None

    async def summarize(self, transcript: str) -> str:
        if not self.client:
            return "Error: Gemini API Key not configured."

        prompt = f"""
        You are a professional meeting secretary. 
        Analyze the following meeting transcript and extract the key information.
        
        Transcript:
        {transcript}
        
        Please provide a structured summary in Markdown format with the following sections:
        
        # Meeting Summary
        (A brief overview of the meeting)
        
        ## Key Discussion Points
        - (Bullet points of main topics discussed)
        
        ## Decisions Made
        - (List of decisions agreed upon)
        
        ## Action Items
        - [ ] (Who) : (What to do)
        
        """
        
        try:
            # Using the async client (aio) to generate content
            response = await self.client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return f"Error generating summary: {e}"

llm_service = LLMService()

