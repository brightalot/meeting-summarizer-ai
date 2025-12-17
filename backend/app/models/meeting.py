import uuid
from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class MeetingStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    status = Column(String, default=MeetingStatus.PENDING.value)
    notion_page_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

