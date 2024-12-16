from typing import Annotated
import asyncio
import random
import json

from aio_pika import IncomingMessage
from pydantic import ValidationError
from sqlalchemy import exc

from src.broker.accessor import BrokerAccessor
from src.schemas import TaskStatus
from src.repository import TaskRepository
from src.database.accessor import AsyncSessionFactory


async def process_task(message: IncomingMessage):
    """Обработчик задач из очереди"""
    async with message.process():
        # Десериализация и валидация данных через Pydantic
        try:
            payload = json.loads(message.body.decode())
            task_id = payload["id"]
            task_name = payload["name"]
            if not task_id or not task_name:
                raise ValueError("Invalid task data")
            
            print(f"Processing task {task_name}")
            async with AsyncSessionFactory() as session:
                try:
                    task_repository = TaskRepository(db_session=session)
                    await task_repository.update_task_status(task_id=task_id, status=TaskStatus.IN_PROGRESS.value)
                    print(f"Task {task_id} is now in progress.")

                    # Эмуляция выполнения задачи
                    await asyncio.sleep(random.randint(5, 10))

                    final_status = random.choice([TaskStatus.COMPLETED.value, TaskStatus.ERROR.value])
                    await task_repository.update_task_status(task_id=task_id, status=final_status)
                    print(f"Task {task_id} status: {final_status}")
                except exc.SQLAlchemyError as error:
                    await session.rollback()
                    print(f"{e}")
        except Exception as e:
            print(f"Error: {e}")

async def run_worker(broker: BrokerAccessor):
    """Запуск воркера."""
    queue = await broker.declare_queue()
    print(f"Worker listening on queue: {queue}")
    await queue.consume(lambda message: process_task(message))