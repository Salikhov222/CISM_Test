from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks

from src.schemas import Task, TaskCreate, TaskStatus
from src.service import TasksService
from src.dependency import get_tasks_service
from src.exceptions import TaskNotFound, DatabaseError
from src.broker.accessor import BrokerAccessor
from src.broker.publisher import publish_task


router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get(
    '/',
    response_model=list[Task]
)
async def get_tasks(
    tasks_service: Annotated[TasksService, Depends(get_tasks_service)],
    status_filter: Annotated[TaskStatus | None, Query(description="Status to filter tasks by")] = None
) -> list[Task]:
    try:
        tasks = await tasks_service.get_all_tasks(status=status_filter) 
        return tasks
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

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
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

@router.post(
    '/',
    response_model=Task,
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    tasks_service: Annotated[TasksService, Depends(get_tasks_service)],
    broker: Annotated[BrokerAccessor, Depends()],
    body: TaskCreate
) -> Task:
    try:
        new_task = await tasks_service.create_task(body)
        await publish_task(broker=broker, task_data=body)
        return new_task
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

# @router.post(
#     '/queue'
# )
# async def create_task_queue(
#     task_data: TaskCreate,
#     broker: Annotated[BrokerAccessor, Depends(get_broker)]
# ) -> dict:
#     try:
#         await publish_task(broker=broker, task_data=task_data)
#         return {"message": "Task accepted", "task_data": task_data}
#     except Exception as e:
#         raise  HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e)
#         )