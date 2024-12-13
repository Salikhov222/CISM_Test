from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import TaskCreate
from src.models import Tasks


class TaskRepository:
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self) -> list[Tasks]:
        tasks: list[Tasks] = (await self.db_session.execute(select(Tasks))).scalars().all()
        return tasks
    
    async def get(self, task_id: int) -> Tasks | None:
        task: Tasks = (await self.db_session.execute(select(Tasks).where(Tasks.id == task_id))).scalar_one_or_none()
        return task
    
    async def add(self, task_data: TaskCreate) -> int:
        query = (
            insert(Tasks)
            .values(title=task_data.title)
            .returning(Tasks.id)
        )
        task_id: int = (await self.db_session.execute(query)).scalar_one_or_none()
        await self.db_session.commit()
        return task_id
    