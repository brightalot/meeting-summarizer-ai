from notion_client import AsyncClient
from app.core.config import settings
from datetime import datetime

class NotionService:
    def __init__(self):
        self.client = AsyncClient(auth=settings.NOTION_API_KEY)
        self.database_id = settings.NOTION_DATABASE_ID

    async def create_meeting_page(self, title: str, summary_markdown: str) -> str:
        """
        Creates a page in the Notion database and returns the URL.
        """
        if not self.database_id:
            print("Notion Database ID not set.")
            return None

        children = []
        
        # Add Summary Body (splitting by paragraphs roughly)
        # Notion block limit is 2000 chars.
        paragraphs = summary_markdown.split("\n\n")
        
        for p in paragraphs:
            if not p.strip(): continue
            
            # Check for headers in markdown to style appropriately (Simple parser)
            if p.startswith("# "):
                block_type = "heading_1"
                content = p[2:]
            elif p.startswith("## "):
                block_type = "heading_2"
                content = p[3:]
            elif p.startswith("### "):
                block_type = "heading_3"
                content = p[4:]
            else:
                block_type = "paragraph"
                content = p

            children.append({
                "object": "block",
                "type": block_type,
                "api_type": {
                    "rich_text": [{"type": "text", "text": {"content": content[:2000]}}]
                }
            })
            # Fix: notion-client uses type name as key, not api_type
            children[-1][block_type] = children[-1].pop("api_type")

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

notion_service = NotionService()

