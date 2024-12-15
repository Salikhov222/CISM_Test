from aio_pika import RobustConnection, connect_robust, Channel, Queue, ExchangeType, Message

from src.config import settings


class BrokerAccessor:
    def __init__(self):
        self._connection: RobustConnection | None = None
        self._channel: Channel | None = None

    async def connect(self):
        """Установить соединение с RabbitMQ и открыть канал"""
        self._connection = await connect_robust(settings.AMQP_URL)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(settings.RABBITMQ_EXCHANGE, ExchangeType.DIRECT)

    async def get_channel(self) -> Channel:
        """Возвращает текущий канал RabbitMQ"""
        if not self._channel:
            raise RuntimeError("Channel is not initialized. Call 'connect()' first.")
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
        await self._exchange.publish(Message(body=message.encode()), routing_key=routing_key)

    async def close(self):
        """Закрыть соединение"""
        if self._channel:
            await self._channel.close()
        if self._connection:
            await self._connection.close()

broker = BrokerAccessor()