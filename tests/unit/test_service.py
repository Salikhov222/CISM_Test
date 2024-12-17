import pytest

from src.exceptions import TaskNotFound, PublishTaskToBroker
from src.config import settings


@pytest.mark.asyncio
async def test_get_all_tasks(tasks_service, mock_task_repository, fake_task):
    """
    Тест на получение всех задач.
    """
    # Настройка
    mock_task_repository.get_all.return_value = [fake_task]

    # Выполнение
    tasks = await tasks_service.get_all_tasks(status=None)

    # Проверка
    assert len(tasks) == 1
    assert tasks[0].id == fake_task.id
    assert tasks[0].title == fake_task.title
    mock_task_repository.get_all.assert_called_once_with(status=None)

@pytest.mark.asyncio
async def test_get_task_by_task_id_found(tasks_service, mock_task_repository, fake_task):
    """
    Тест на успешное получение задачи по ID.
    """
    # Настройка
    mock_task_repository.get_task.return_value = fake_task

    # Выполнение
    task = await tasks_service.get_task_by_task_id(task_id=1)

    # Проверка
    assert task.id == fake_task.id
    assert task.title == fake_task.title
    mock_task_repository.get_task.assert_called_once_with(task_id=1)

@pytest.mark.asyncio
async def test_get_task_by_task_id_not_found(tasks_service, mock_task_repository):
    """
    Тест на ошибку, если задача с указанным ID не найдена.
    """
    # Настройка
    mock_task_repository.get_task.return_value = None

    # Выполнение и проверка
    with pytest.raises(TaskNotFound):
        await tasks_service.get_task_by_task_id(task_id=999)
    mock_task_repository.get_task.assert_called_once_with(task_id=999)

@pytest.mark.asyncio
async def test_create_task_success(tasks_service, mock_task_repository, mock_broker, fake_task_data, fake_task):
    """
    Тест на успешное создание задачи и публикацию в очередь.
    """
    # Настройка
    mock_task_repository.create_task.return_value = fake_task

    # Выполнение
    task = await tasks_service.create_task(task_data=fake_task_data)

    # Проверка
    assert task.id == fake_task.id
    assert task.title == fake_task.title
    mock_task_repository.create_task.assert_called_once_with(task_data=fake_task_data)
    mock_broker.publish_message.assert_called_once_with(
        message={"id": fake_task.id, "name": fake_task.title},
        routing_key=settings.RABBITMQ_QUEUE
    )

@pytest.mark.asyncio
async def test_create_task_broker_fail(tasks_service, mock_task_repository, mock_broker, fake_task_data, fake_task):
    """
    Тест на ошибку при публикации сообщения в брокер.
    """
    # Настройка
    mock_task_repository.create_task.return_value = fake_task
    mock_broker.publish_message.side_effect = Exception("Broker error")

    # Выполнение и проверка
    with pytest.raises(PublishTaskToBroker):
        await tasks_service.create_task(task_data=fake_task_data)

    mock_task_repository.create_task.assert_called_once_with(task_data=fake_task_data)
    mock_broker.publish_message.assert_called_once_with(
        message={"id": fake_task.id, "name": fake_task.title},
        routing_key=settings.RABBITMQ_QUEUE
    )