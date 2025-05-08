from uuid import UUID, uuid4
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from redis.asyncio import Redis
import os, json, httpx

redis = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

class ProjectIn(BaseModel):
    title: str = Field(..., example="市场营销策略")
    outline: str | None = None
    template_style: str | None = None

class ProjectOut(BaseModel):
    id: UUID
    status: str

router = APIRouter()

@router.post("/", response_model=ProjectOut)
async def create_project(data: ProjectIn, bg: BackgroundTasks):
    pid = uuid4()
    await redis.hset(f"project:{pid}", mapping={
        "title": data.title,
        "status": "queued"
    })
    bg.add_task(trigger_generation, pid, data.model_dump())
    return ProjectOut(id=pid, status="queued")

async def trigger_generation(pid: UUID, payload: dict):
    async with httpx.AsyncClient() as client:
        await client.post("<http://worker:8000/trigger>", json={"id": str(pid), **payload})
