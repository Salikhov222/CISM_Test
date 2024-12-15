from collections.abc import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.config import settings
from src.exceptions import DatabaseError


engine = create_async_engine(
    settings.get_postgres_uri.unicode_string(),
    echo=True,   # логирование запросов
    pool_pre_ping=True
    )

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)

# Функция для системы зависимостей Depends, которая устанавливает связь между логикой и конфигурацией БД
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise DatabaseError(f'Database error occurred')

    