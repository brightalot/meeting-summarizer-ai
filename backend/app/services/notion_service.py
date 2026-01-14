from notion_client import AsyncClient
from app.core.config import settings
from datetime import datetime

class NotionService:
    def __init__(self):
        if settings.NOTION_API_KEY:
            self.client = AsyncClient(auth=settings.NOTION_API_KEY)
        else:
            print("Warning: NOTION_API_KEY is not set.")
            self.client = None
        self.database_id = settings.NOTION_DATABASE_ID

    async def create_meeting_page(self, title: str, summary_markdown: str) -> str:
        """
        Creates a page in the Notion database and returns the URL.
        """
        if not self.client:
            print("Notion Client not initialized.")
            return None

        if not self.database_id:
            print("Notion Database ID not set.")
            return None

        children = []
        
        # 개선된 마크다운 파싱
        lines = summary_markdown.split("\n")
        current_paragraph = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # 빈 줄 처리
            if not line_stripped:
                if current_paragraph:
                    # 현재 단락을 블록으로 추가
                    paragraph_text = " ".join(current_paragraph).strip()
                    if paragraph_text:
                        children.append(self._create_paragraph_block(paragraph_text))
                    current_paragraph = []
                continue
            
            # 헤더 처리
            if line_stripped.startswith("# "):
                if current_paragraph:
                    paragraph_text = " ".join(current_paragraph).strip()
                    if paragraph_text:
                        children.append(self._create_paragraph_block(paragraph_text))
                    current_paragraph = []
                children.append(self._create_heading_block("heading_1", line_stripped[2:]))
            elif line_stripped.startswith("## "):
                if current_paragraph:
                    paragraph_text = " ".join(current_paragraph).strip()
                    if paragraph_text:
                        children.append(self._create_paragraph_block(paragraph_text))
                    current_paragraph = []
                children.append(self._create_heading_block("heading_2", line_stripped[3:]))
            elif line_stripped.startswith("### "):
                if current_paragraph:
                    paragraph_text = " ".join(current_paragraph).strip()
                    if paragraph_text:
                        children.append(self._create_paragraph_block(paragraph_text))
                    current_paragraph = []
                children.append(self._create_heading_block("heading_3", line_stripped[4:]))
            # 불릿 포인트 처리
            elif line_stripped.startswith("- "):
                if current_paragraph:
                    paragraph_text = " ".join(current_paragraph).strip()
                    if paragraph_text:
                        children.append(self._create_paragraph_block(paragraph_text))
                    current_paragraph = []
                # 체크박스 처리 ([ ] 또는 [x])
                if line_stripped.startswith("- [ ]") or line_stripped.startswith("- [x]"):
                    checkbox_text = line_stripped[5:].strip()
                    is_checked = line_stripped.startswith("- [x]")
                    children.append(self._create_checkbox_block(checkbox_text, is_checked))
                else:
                    # 일반 불릿 포인트
                    bullet_text = line_stripped[2:].strip()
                    children.append(self._create_bullet_block(bullet_text))
            else:
                # 일반 텍스트 (단락에 추가)
                current_paragraph.append(line_stripped)
        
        # 마지막 단락 처리
        if current_paragraph:
            paragraph_text = " ".join(current_paragraph).strip()
            if paragraph_text:
                children.append(self._create_paragraph_block(paragraph_text))
        
        try:
            response = await self.client.pages.create(
                parent={"database_id": self.database_id},
                properties={
                    "Name": {"title": [{"text": {"content": title}}]},
                    "Date": {"date": {"start": datetime.now().isoformat()}}
                },
                children=children
            )
            return response["url"]
        except Exception as e:
            print(f"Notion API Error: {e}")
            return None
    
    def _create_paragraph_block(self, text: str) -> dict:
        """단락 블록 생성"""
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }
    
    def _create_heading_block(self, heading_type: str, text: str) -> dict:
        """헤더 블록 생성"""
        return {
            "object": "block",
            "type": heading_type,
            heading_type: {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }
    
    def _create_bullet_block(self, text: str) -> dict:
        """불릿 포인트 블록 생성"""
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }
    
    def _create_checkbox_block(self, text: str, checked: bool = False) -> dict:
        """체크박스 블록 생성 (액션 아이템용)"""
        return {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}],
                "checked": checked
            }
        }

notion_service = NotionService()

