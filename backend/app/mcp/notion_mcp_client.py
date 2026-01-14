"""
Notion MCP Client

FastAPI 애플리케이션에서 MCP를 통해 Notion과 상호작용하는 클라이언트
"""
from app.core.config import settings
from app.services.notion_service import notion_service
from typing import Optional
import asyncio

class NotionMCPClient:
    """Notion MCP 클라이언트"""
    
    def __init__(self):
        self.notion_service = notion_service
    
    async def create_meeting_page(self, title: str, summary_markdown: str) -> Optional[str]:
        """
        MCP를 통해 Notion 페이지 생성
        
        Args:
            title: 회의 제목
            summary_markdown: 마크다운 형식의 요약 내용
            
        Returns:
            생성된 Notion 페이지 URL 또는 None
        """
        # NotionService를 통해 Notion API 호출
        return await self.notion_service.create_meeting_page(title, summary_markdown)
    
    async def get_database_info(self) -> Optional[dict]:
        """
        MCP를 통해 Notion 데이터베이스 정보 조회
        
        Returns:
            데이터베이스 정보 딕셔너리 또는 None
        """
        if not self.notion_service.client:
            return None
        
        if not self.notion_service.database_id:
            return None
        
        try:
            db_info = await self.notion_service.client.databases.retrieve(
                database_id=self.notion_service.database_id
            )
            return {
                "id": self.notion_service.database_id,
                "title": db_info.get("title", [{}])[0].get("plain_text", "N/A") if db_info.get("title") else "N/A"
            }
        except Exception as e:
            print(f"Error retrieving database info: {e}")
            return None

# 싱글톤 인스턴스
notion_mcp_client = NotionMCPClient()

