from google import genai
from app.core.config import settings
from app.mcp.notion_mcp_client import notion_mcp_client
from typing import Optional, Tuple
import json

class LLMService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            # Initialize the client from google-genai SDK
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        else:
            print("Warning: GEMINI_API_KEY is not set.")
            self.client = None

    def _get_notion_tools(self) -> list:
        """Gemini Function Calling을 위한 Notion 도구 정의"""
        return [
            {
                "function_declarations": [
                    {
                        "name": "create_meeting_page",
                        "description": "회의 요약을 Notion 데이터베이스에 새 페이지로 생성합니다. 요약을 생성한 후 반드시 이 함수를 호출하여 Notion에 저장해야 합니다.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "회의 제목 (예: '2024년 1월 15일 스프린트 회의')"
                                },
                                "summary_markdown": {
                                    "type": "string",
                                    "description": "마크다운 형식의 회의 요약 내용. 회의 요약, 주요 논의 사항, 결정된 사항, 액션 아이템을 포함해야 합니다."
                                }
                            },
                            "required": ["title", "summary_markdown"]
                        }
                    }
                ]
            }
        ]

    async def _handle_function_call(self, function_name: str, arguments: dict) -> str:
        """함수 호출 처리"""
        if function_name == "create_meeting_page":
            title = arguments.get("title", "")
            summary_markdown = arguments.get("summary_markdown", "")
            
            if not title or not summary_markdown:
                return "Error: title and summary_markdown are required"
            
            try:
                notion_url = await notion_mcp_client.create_meeting_page(title, summary_markdown)
                if notion_url:
                    return f"Successfully created Notion page: {notion_url}"
                else:
                    return "Error: Failed to create Notion page. Check logs and configuration."
            except Exception as e:
                return f"Error creating Notion page: {str(e)}"
        
        return f"Unknown function: {function_name}"

    async def summarize_and_save_to_notion(self, transcript: str, meeting_title: str) -> Tuple[str, Optional[str]]:
        """
        회의록을 요약하고 자동으로 Notion에 저장합니다.
        
        Returns:
            (summary_text, notion_url) 튜플
        """
        if not self.client:
            return ("Error: Gemini API Key not configured.", None)

        prompt = f"""
        You are a professional meeting secretary. 
        Analyze the following meeting transcript and extract the key information.
        
        Meeting Title: {meeting_title}
        Transcript:
        {transcript}
        
        Please create a structured summary in Markdown format. Follow this EXACT format and structure:
        
        # 회의 요약
        
        (회의에 대한 간략한 2-3문장 개요를 작성하세요)
        
        ## 주요 논의 사항
        
        - (첫 번째 논의 주제)
        - (두 번째 논의 주제)
        - (세 번째 논의 주제)
        
        ## 결정된 사항
        
        - (첫 번째 결정 사항)
        - (두 번째 결정 사항)
        
        ## 액션 아이템
        
        - [ ] (담당자명) : (구체적인 할 일 내용)
        - [ ] (담당자명) : (구체적인 할 일 내용)
        
        **Important formatting rules:**
        1. Use exactly one blank line between sections (##)
        2. Use exactly one blank line before and after bullet lists
        3. Each bullet point should be on a new line starting with "- "
        4. Action items must use the format: "- [ ] (담당자) : (내용)"
        5. Keep each section clearly separated with blank lines
        6. Use Korean language for all content
        7. Do not add extra blank lines or formatting
        """
        
        try:
            # Gemini로 요약 생성
            response = await self.client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            
            summary_text = response.text if hasattr(response, 'text') else ""
            
            # 요약 생성 후 자동으로 Notion에 저장
            notion_url = None
            if summary_text:
                print(f"Summary generated. Now creating Notion page...")
                try:
                    notion_url = await notion_mcp_client.create_meeting_page(meeting_title, summary_text)
                    if notion_url:
                        print(f"Successfully created Notion page: {notion_url}")
                    else:
                        print("Warning: Failed to create Notion page. Check logs and configuration.")
                except Exception as e:
                    print(f"Error creating Notion page: {e}")
                    import traceback
                    traceback.print_exc()
            
            return (summary_text, notion_url)
            
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            import traceback
            traceback.print_exc()
            return (f"Error generating summary: {e}", None)

    async def summarize(self, transcript: str) -> str:
        """기존 호환성을 위한 메서드 (Function Calling 없이)"""
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
        """
        
        try:
            response = await self.client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return f"Error generating summary: {e}"

llm_service = LLMService()

