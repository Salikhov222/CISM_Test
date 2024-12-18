import json 

from aio_pika import connect_robust, Channel, Queue, ExchangeType, Message
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractExchange

from src.config import settings

AMQP_URL = f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/"

class BrokerAccessor:
    def __init__(self):
        self._connection: AbstractConnection | None = None
        self._channel: AbstractChannel | None = None
        self._exchange: AbstractExchange | None = None

    async def connect(self):
        """Установить соединение с RabbitMQ и открыть канал"""
        try:
            self._connection = await connect_robust(AMQP_URL)
            self._channel = await self._connection.channel()
            await self._channel.set_qos(prefetch_count=5)
            self._exchange = await self._channel.declare_exchange(settings.RABBITMQ_EXCHANGE, type=ExchangeType.DIRECT, durable=True)
        except Exception as e:
            raise RuntimeError(f"Broker connection failed {e}")

    async def get_channel(self) -> Channel:
        """Возвращает текущий канал RabbitMQ"""

        if not self._channel or self._channel.is_closed:
            await self.connect()
        return self._channel
    
    async def declare_queue(self) -> Queue:
        """Создать очередь"""

        channel = await self.get_channel()
        queue =  await channel.declare_queue(settings.RABBITMQ_QUEUE, durable=True)
        await queue.bind(self._exchange, routing_key=settings.RABBITMQ_QUEUE)
        return queue
    
    async def publish_message(self, routing_key: str, message: str):
        """Публиковать сообщение"""

        if not self._exchange:
            raise RuntimeError("Exchange is not declared. Call 'connect()' first.")
        serialized_message = json.dumps(message)
        await self._exchange.publish(Message(body=serialized_message.encode(), delivery_mode=2), routing_key=routing_key)

    async def close(self):
        """Закрыть соединение"""

        if self._channel:
            await self._channel.close()
        if self._connection:
            await self._connection.close()

broker = BrokerAccessor()