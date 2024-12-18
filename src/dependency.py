from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database import get_session
from src.tasks.repository import TaskRepository
from src.tasks.service import TasksService
from src.infrastructure.broker.accessor import BrokerAccessor, broker
from src.config import settings


async def get_task_repository(
    db_session: Annotated[AsyncSession, Depends(get_session)]
) -> TaskRepository:
    return TaskRepository(db_session=db_session)

async def get_broker() -> BrokerAccessor:
    await broker.connect()
    return broker

async def get_tasks_service(
    task_repository: Annotated[TaskRepository, Depends(get_task_repository)],
    broker: Annotated[BrokerAccessor, Depends(get_broker)]
) -> TasksService:
    return TasksService(
        task_repository=task_repository, 
        broker=broker
    )

