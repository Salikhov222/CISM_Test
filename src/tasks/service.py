from src.tasks.repository import TaskRepository
from src.tasks.schemas import Task, TaskCreate
from src.exceptions import TaskNotFound, PublishTaskToBroker
from src.infrastructure.broker.accessor import BrokerAccessor
from src.config import settings


class TasksService:

    def __init__(self, task_repository: TaskRepository, broker: BrokerAccessor):
        self.task_repository = task_repository
        self.broker = broker

    async def get_all_tasks(self, status: str | None) -> list[Task]:
        tasks = await self.task_repository.get_all(status=status)
        tasks_schema = [Task.model_validate(task) for task in tasks]
        return tasks_schema
    
    async def get_task_by_task_id(self, task_id: int) -> Task:
        task = await self.task_repository.get_task(task_id=task_id)
        if not task:
            raise TaskNotFound(f'Task {task_id} not found')
        return Task.model_validate(task)
    
    async def create_task(self, task_data: TaskCreate) -> Task:
        task = await self.task_repository.create_task(task_data=task_data)
        
        try:
            await self.broker.publish_message(
                message={
                    "id": task.id,
                    "name": task.title
                },
                routing_key=settings.RABBITMQ_QUEUE
            )
        except Exception as e:
            raise PublishTaskToBroker("The task was created but could not be queued.")
        return Task.model_validate(task)
    
