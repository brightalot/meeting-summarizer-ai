from app.core.database import SessionLocal
from app.models.meeting import Meeting, MeetingStatus
from app.services.stt_service import stt_service
from app.services.llm_service import llm_service
import uuid

async def run_pipeline(meeting_id: uuid.UUID):
    async with SessionLocal() as db:
        meeting = await db.get(Meeting, meeting_id)
        if not meeting:
            print(f"Meeting {meeting_id} not found in background task.")
            return

        meeting.status = MeetingStatus.PROCESSING.value
        await db.commit()

        try:
            # Step 1: STT
            print(f"Starting transcription for meeting {meeting_id}...")
            transcript = await stt_service.transcribe(meeting.file_path)
            meeting.transcript = transcript
            print(f"Transcription completed for meeting {meeting_id}.")
            
            # Save progress
            await db.commit()
            
            # Step 2: LLM 요약 생성 및 자동 Notion 저장
            print(f"Starting summarization and automatic Notion creation for meeting {meeting_id}...")
            summary, notion_url = await llm_service.summarize_and_save_to_notion(transcript, meeting.title)
            meeting.summary = summary
            
            if notion_url:
                meeting.notion_page_url = notion_url
                print(f"Notion page created automatically: {notion_url}")
            else:
                print("Warning: Notion page creation failed. Summary generated but Notion page was not created.")
            
            print(f"Summarization completed for meeting {meeting_id}.")
            await db.commit()

            meeting.status = MeetingStatus.COMPLETED.value
            await db.commit()
            
        except Exception as e:
            print(f"Pipeline failed for {meeting_id}: {e}")
            meeting.status = MeetingStatus.FAILED.value
            await db.commit()

