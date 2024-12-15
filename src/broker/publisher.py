import json

from src.broker.accessor import BrokerAccessor
from src.schemas import TaskCreate
from src.config import settings


async def publish_task(broker: BrokerAccessor, task_data: TaskCreate):
    """Публикация задачи в очередь"""
    message = TaskCreate.model_dump_json(task_data)

    await broker.publish_message(
        routing_key=settings.RABBITMQ_QUEUE,
        message=message
    )