import logging
import uuid

from fastapi import APIRouter
from workspace.repos.ai_repo import AI_Repo
from workspace.dto.requests import GeneratingRequest
from workspace.services.worker import sort_data

main_router = APIRouter()

logger = logging.getLogger(__name__)


@main_router.post("/generate")
async def generate_text(data: GeneratingRequest):
    logger.info(f"Generating text for prompt: {data.prompt}")
    generated_text = sort_data.delay(data.data)
    return {
        "status": "success",
        "prompt": data.prompt,
        "task_id": generated_text.id,
        "details": "Task has been accepted for processing by Celery worker.",

    }

@main_router.get("/task/{task_id}")
async def get_task_status(task_id: uuid.UUID):
    logger.info(f"Getting status for task: {task_id}")
    task_result = await AI_Repo.get_output_by_id(task_id)
    return {
        "task_id": str(task_id),
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else "Pending"
    }