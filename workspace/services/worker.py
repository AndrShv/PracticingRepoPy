import asyncio
import json
import logging

from google import genai
from workspace.configs.main_config import settings
from workspace.configs.celery_config import celery_app
from workspace.helpers.json_cleaner import clean_json

logger = logging.getLogger(__name__)
GEMINI_MODEL = "gemini-3.6-flash"


async def process_task(data: dict[str, str]):
    logger.info(f"Начало обработки задачи с данными: {data.__sizeof__()}")
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    prompt = ""

    try:
        response = await client.aio.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        raw_text = response.text.strip()
        cleaned_text = await clean_json(raw_text)
        result = json.loads(cleaned_text)
        logger.info(f"Результат обработки задачи: {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при генерации контента с использованием модели Gemini: {e}")
        raise Exception("Ошибка при генерации контента с использованием модели Gemini.")



@celery_app.task(name="workspace.services.worker.process_task")
def sort_data(data: dict[str, str]):
    logger.info(f"Запуск Celery задачи для обработки данных: {data.__sizeof__()}")
    try:
        logger.info(f"Начало выполнения задачи с данными: {data.__sizeof__()}")
        asyncio.run(process_task(data))
    except Exception as e:
        logger.error(f"Ошибка при выполнении задачи: {e}")
        raise
