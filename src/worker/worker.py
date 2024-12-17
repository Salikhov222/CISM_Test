import logging
import asyncio
import random
import json

from aio_pika import IncomingMessage
from sqlalchemy import exc

from src.broker.accessor import BrokerAccessor, broker
from src.schemas import TaskStatus
from src.repository import TaskRepository
from src.database.accessor import AsyncSessionFactory


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def process_task(message: IncomingMessage):
    """Обработчик задач из очереди"""
    async with message.process():
        # Десериализация и валидация данных через Pydantic
        try:
            logging.info(f"Received message {message.body.decode()}")
            payload = json.loads(message.body.decode())
            task_id = payload["id"]
            task_name = payload["name"]
            if not task_id or not task_name:
                raise ValueError("Invalid task data")
            
            logging.info(f"Processing task: id={task_id}, name={task_name}")
            async with AsyncSessionFactory() as session:
                try:
                    task_repository = TaskRepository(db_session=session)
                    await task_repository.update_task_status(task_id=task_id, status=TaskStatus.IN_PROGRESS.value)
                    logging.info(f"Task {task_id} is now in progress.")

                    # Эмуляция выполнения задачи
                    await asyncio.sleep(random.randint(5, 10))

                    final_status = random.choice([TaskStatus.COMPLETED.value, TaskStatus.ERROR.value])
                    await task_repository.update_task_status(task_id=task_id, status=final_status)
                    logging.info(f"Task {task_id} completed successfully. Status: {final_status}")
                except exc.SQLAlchemyError as error:
                    await session.rollback()
                    logging.error(f"Database error: {e}")
        except Exception as e:
            logging(f"Error: {e}")

async def run_worker(broker: BrokerAccessor):
    """Запуск воркера."""
    queue = await broker.declare_queue()
    logging.info(f"Worker listening on queue: {queue}")
    await queue.consume(lambda message: process_task(message))

    try:
        await asyncio.Future()  # поддерживание брокера активным
    finally:
        await broker.close()

if __name__ == "__main__":
    asyncio.run(run_worker(broker=broker))