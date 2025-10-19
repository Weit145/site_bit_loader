from app.core.config import settings

from celery import Celery

app = Celery(
    main = "app.tasks.celery",
    broker = settings.broker,
    backend="rpc://"
)