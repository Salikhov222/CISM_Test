import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.repository.tasks import TaskRepository
from src.broker.worker import run_worker
from src.routes.tasks import router as task_router
from src.broker.accessor import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения."""
    # Подключаемся к RabbitMQ
    await broker.connect()
    await broker.declare_queue()
    task_repository = TaskRepository()

    print("Connected to RabbitMQ")

    # Запускаем воркера в фоновом режиме
    worker_task = asyncio.create_task(run_worker(broker,task_repository))
    print("Worker started")

    try:
        yield  # Успешный запуск приложения
    finally:
        # Завершаем воркера и закрываем соединение
        worker_task.cancel()
        await broker.close()
        print("RabbitMQ connection closed")

app =  FastAPI(lifespan=lifespan)
app.include_router(task_router)

