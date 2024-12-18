from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import TaskNotFound
from src.tasks.schemas import TaskCreate
from src.tasks.models import Tasks


class TaskRepository:
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, status: str | None) -> list[Tasks]:
        query = select(Tasks)
        if status:
            query = query.where(Tasks.status == status)
        tasks: list[Tasks] = (await self.db_session.execute(query)).scalars().all()
        return tasks
    
    async def get_task(self, task_id: int) -> Tasks | None:
        task: Tasks = (await self.db_session.execute(select(Tasks).where(Tasks.id == task_id))).scalar_one_or_none()
        return task
    
    async def create_task(self, task_data: TaskCreate) -> Tasks:
        query = (
            insert(Tasks)
            .values(title=task_data.title, status='new')
            .returning(Tasks)
        )
        task: Tasks = (await self.db_session.execute(query)).scalar_one_or_none()
        await self.db_session.commit()
        return task
    
    async def update_task_status(self, task_id: int, status: str) -> None:
        task = await self.get_task(task_id=task_id)
        if not task:
            raise TaskNotFound(f'Task {task_id} not found')
        task.status = status
        await self.db_session.commit()

    