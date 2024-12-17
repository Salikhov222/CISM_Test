from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    # AMQP_URL: str = 'amqp://guest:guest@rabbitmq:5672//'
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int = 5672
    RABBITMQ_QUEUE: str = "tasks_queue"
    RABBITMQ_EXCHANGE: str = "tasks_exchange" 

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
    @computed_field
    @property
    def get_postgres_uri(self) -> PostgresDsn:
        """
        Это вычисляемое, при каждом доступе, свойство объекта, которое генерирует URL-адрес для подключения к БД
        Является ленивым, то есть адрес будет построен только тогда, когда вызывается данное свойство

        Принимает следующие параметры:
        - scheme: Схема URL. В данном случае это "postgresql+asyncpg"
        - username: Имя пользователя БД
        - password: Пароль пользователя БД
        - host: Хост подключения к БД
        - path: Имя БД

        Returns:
            PostgresDsn: Сконструированный URL PostgresDsn для asyncpg
        """

        required_env_vars = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_DB']
        for var in required_env_vars:
            if not getattr(self, var, None):
                raise ValueError(f'Отсутствует требуемая переменная окружения: {var}')
            
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        )

settings = Settings()