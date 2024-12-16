from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks

from src.schemas import Task, TaskCreate, TaskStatus, ErrorSchema
from src.service import TasksService
from src.dependency import get_tasks_service
from src.exceptions import TaskNotFound, PublishTaskToBroker


router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get(
    '/',
    response_model=list[Task],
    status_code=status.HTTP_200_OK,
    description="Получение списка всех задач",
    responses={
        status.HTTP_200_OK: {"model": list[Task]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorSchema}
    }
)
async def get_tasks(
    tasks_service: Annotated[TasksService, Depends(get_tasks_service)],
    status_filter: Annotated[TaskStatus | None, Query(description="Status to filter tasks by")] = None
) -> list[Task]:
    """Получение списка всех задач"""
    try:
        tasks = await tasks_service.get_all_tasks(status=status_filter) 
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    '/{id}',
    response_model=Task,
    status_code=status.HTTP_200_OK,
    description="Получение определенной задачи по ее номеру",
    responses={
        status.HTTP_200_OK: {"model": Task},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema}
    }
)
async def get_task(
    tasks_service: Annotated[TasksService, Depends(get_tasks_service)],
    id: int
) -> Task:
    """Получение данных задачи по ее id"""
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
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    description="Создание новой задачи",
    responses={
        status.HTTP_201_CREATED: {"model": Task},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ErrorSchema}
    }
)
async def create_task(
    tasks_service: Annotated[TasksService, Depends(get_tasks_service)],
    body: TaskCreate
) -> Task:
    """Создание новой задачи"""
    try:
        new_task = await tasks_service.create_task(body)
        return new_task
    except PublishTaskToBroker as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
