from typing import Annotated
import asyncio
import random

from aio_pika import IncomingMessage
from pydantic import ValidationError

from src.broker.accessor import BrokerAccessor
from src.schemas import TaskCreate, TaskStatus
from src.repository import TaskRepository


async def process_task(message: IncomingMessage, task_repository: TaskRepository):
    """Обработчик задач из очереди"""
    async with message.process():
        # Десериализация и валидация данных через Pydantic
        try:
            task_id = message["id"]
            task_name = message["name"]
            print(f"Processing task {task_name}")

            await task_repository.update_task_status(task_id=task_id, status=TaskStatus.IN_PROGRESS.value)
            print(f"Task {task_id} is now in progress.")

            # Эмуляция выполнения задачи
            await asyncio.sleep(random.randint(5, 10))

            final_status = random.choice([TaskStatus.COMPLETED.value, TaskStatus.ERROR.value])
            await task_repository.update_task_status(task_id=task_id, status=final_status)
            print(f"Task {task_id} status: {final_status}")
        except ValidationError as e:
            print(f"Validation error for message {message.body}: {e}")
        except Exception as e:
            print(f"Error: {e}")

async def run_worker(broker: BrokerAccessor, task_repository: TaskRepository):
    """Запуск воркера."""
    queue = await broker.declare_queue()
    print(f"Worker listening on queue: {queue}")
    await queue.consume(lambda message: process_task(message, task_repository))