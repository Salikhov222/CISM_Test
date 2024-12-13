from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.repository import TaskRepository
from src.service import TasksService


async def get_task_repository(
    db_session: Annotated[AsyncSession, Depends(get_session)]
) -> TaskRepository:
    return TaskRepository(db_session=db_session)

async def get_tasks_service(
    task_repository: Annotated[TaskRepository, Depends(get_task_repository)]
) -> TasksService:
    return TasksService(task_repository=task_repository)