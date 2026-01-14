from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.meeting import Meeting, MeetingStatus
from app.services.pipeline import run_pipeline
import shutil
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/meetings/upload")
async def upload_meeting(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_meeting = Meeting(
        title=file.filename,
        file_path=file_path,
        status=MeetingStatus.PENDING.value
    )
    db.add(new_meeting)
    await db.commit()
    await db.refresh(new_meeting)

    # Trigger background processing
    background_tasks.add_task(run_pipeline, new_meeting.id)
    
    return {"id": str(new_meeting.id), "status": new_meeting.status}

@router.get("/meetings/{meeting_id}")
async def get_meeting(meeting_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    meeting = await db.get(Meeting, meeting_id)
    return meeting

