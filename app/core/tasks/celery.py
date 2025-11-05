from celery import Celery

from app.core.config import settings

app = Celery(
    "app/core",
    broker = settings.broker,
    backend="rpc://",
)

app.autodiscover_tasks(["app.core.tasks"])
