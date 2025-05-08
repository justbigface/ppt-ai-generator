from fastapi import APIRouter
from .routers import projects

router = APIRouter()
router.include_router(projects.router, prefix="/projects", tags=["projects"])
