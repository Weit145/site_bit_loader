from app.core.config import settings

from celery import Celery

app = Celery(
    "app",
    broker = settings.broker,
    backend="rpc://",
)

app.autodiscover_tasks(["app.tasks"])
