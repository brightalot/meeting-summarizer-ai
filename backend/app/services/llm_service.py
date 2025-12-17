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
        
        Please provide a structured summary in Markdown format with the following sections in Korean:
        
        # 회의 요약
        (회의에 대한 간략한 개요)
        
        ## 주요 논의 사항
        - (논의된 주요 주제에 대한 글머리 기호)
        
        ## 결정된 사항
        - (합의된 결정 목록)
        
        ## 액션 아이템
        - [ ] (담당자) : (할 일)
        
        Example Output Format:
        # 회의 요약
        ...
        ## 주요 논의 사항
        - ...
        ## 결정된 사항
        - ...
        ## 액션 아이템
        - [ ] ...
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

