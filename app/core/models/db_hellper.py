from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from ..config import settings


class DatabaseHellper:
    def __init__(self, url: str, echo: bool = False):
        # Создаем асинхронный движок для подключения к БД
        self.engine = create_async_engine(url=url, echo=echo)
        # Создаем фабрику асинхронных сессий
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        # Создаем scoped сессию - одна сессия на одну асинхронную задачу
        session = async_scoped_session(
            session_factory=self.session_factory, scopefunc=current_task
        )
        return session

    async def session_dependency(self):
        # Генератор сессий для зависимостей FastAPI
        session = self.get_scoped_session()
        try:
            yield session
        finally:
            await session.close()


# Создаем глобальный экземпляр помощника БД с настройками из конфига
db_helper = DatabaseHellper(url=settings.db_url, echo=settings.db_echo)
