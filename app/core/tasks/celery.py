from celery import Celery

from app.core.config import settings

app = Celery(
    "app",
    broker = settings.broker,
    backend="rpc://",
)

app.autodiscover_tasks(["app.tasks"])
