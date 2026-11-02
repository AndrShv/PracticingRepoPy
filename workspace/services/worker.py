import asyncio

from workspace.configs.celery_config import celery_app


async def process_task(data: dict[str, str]):
    await asyncio.sleep(5)
    print("Task completed!")

@celery_app.task(name="workspace.services.worker.process_task")
def sort_data(data: dict[str, str]):
    try:
        asyncio.run(process_task(data))
    except Exception as e:
        print(f"Ошибка при выполнении задачи: {e}")
        raise
