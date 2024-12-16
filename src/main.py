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
    try:
        await broker.connect()
        await broker.declare_queue()

        print("Connected to RabbitMQ")

    except Exception as e:
        raise RuntimeError("No connection to broker") from e
    # Запускаем воркера в фоновом режиме
    worker_task = asyncio.create_task(run_worker(broker))
    print("Worker started")

    try:
        yield  # Успешный запуск приложения
    finally:
        # Завершаем воркера и закрываем соединение
        worker_task.cancel()
        await broker.close()
        print("RabbitMQ connection closed")

app =  FastAPI(
    title="Task management service",
    summary="Simple task management service",
    lifespan=lifespan
    )

app.include_router(task_router)

