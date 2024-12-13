from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas import Task, TaskCreate
from src.service import TasksService
from src.dependency import get_tasks_service
from src.exceptions import TaskNotFound


router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get(
    '/',
    response_model=list[Task]
)
async def get_tasks(
    tasks_service: Annotated[TasksService, Depends(get_tasks_service)] 
) -> list[Task]:
    tasks = await tasks_service.get_all_tasks() 
    return tasks

@router.get(
    '/{id}',
    response_model=Task
)
async def get_task(
    tasks_service: Annotated[TasksService, Depends(get_tasks_service)],
    id: int
) -> Task:
    try:
        task = await tasks_service.get_task_by_task_id(task_id=id)
        return task
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post(
    '/',
    response_model=Task
)
async def create_task(
    tasks_service: Annotated[TasksService, Depends(get_tasks_service)],
    body: TaskCreate
) -> Task:
    create_task = await tasks_service.create_task(body)
    return create_task