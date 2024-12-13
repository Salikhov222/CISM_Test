from src.repository import TaskRepository
from src.schemas import Task, TaskCreate
from src.exceptions import TaskNotFound


class TasksService:

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def get_all_tasks(self) -> list[Task]:
        tasks = await self.task_repository.get_all()
        tasks_schema = [Task.model_validate(task) for task in tasks]
        return tasks_schema
    
    async def get_task_by_task_id(self, task_id: int) -> Task:
        task = await self.task_repository.get(task_id=task_id)
        if not task:
            raise TaskNotFound(f'Task {task_id} not found')
        return Task.model_validate(task)
    
    async def create_task(self, task_data: TaskCreate) -> Task:
        task_id = await self.task_repository.add(task_data=task_data)
        task = await self.task_repository.get(task_id=task_id)
        return Task.model_validate(task)