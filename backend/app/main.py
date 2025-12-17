from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
from app.api.meetings import router as meetings_router

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
async def startup():
    # In production, use Alembic for migrations. 
    # For MVP simplicity, we can create tables here if they don't exist.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(meetings_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to NoteSync AI API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

