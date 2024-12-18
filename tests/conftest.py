import pytest
import datetime

from unittest.mock import AsyncMock

from src.tasks.service import TasksService
from src.tasks.schemas import Task, TaskCreate


@pytest.fixture
def mock_task_repository():
    """
    Фикстура для мокированного репозитория задач.
    """
    mock_repo = AsyncMock()
    return mock_repo

@pytest.fixture
def mock_broker():
    """
    Фикстура для мокированного брокера.
    """
    mock_broker = AsyncMock()
    return mock_broker

@pytest.fixture
def tasks_service(mock_task_repository, mock_broker):
    """
    Фикстура для инициализации сервисного слоя задач.
    """
    return TasksService(task_repository=mock_task_repository, broker=mock_broker)

@pytest.fixture
def fake_task():
    """
    Фикстура для тестовой задачи.
    """
    return Task(id=1, 
        title="Test Task", 
        status="new", 
        created_at=datetime.datetime.now(), 
        updated_at=datetime.datetime.now()
    )

@pytest.fixture
def fake_task_data():
    """
    Фикстура для данных, используемых при создании новой задачи.
    """
    return TaskCreate(title="New Test Task")

