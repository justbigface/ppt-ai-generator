import os
from celery import Celery

celery_app = Celery(
    "ppt_ai_worker",
    broker=os.getenv("BROKER_URL", "redis://redis:6379/1"),
    backend=os.getenv("RESULT_BACKEND", "redis://redis:6379/2"),
)

celery_app.autodiscover_tasks(["worker.tasks"])
