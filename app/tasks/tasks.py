from app.tasks.celery import app
import asyncio
from pathlib import Path

from app.tasks.email.email import send_email

@app.task(name="send_email")
def send_message():
    html_path = Path("app/templates/pod_reg.html")
    html_content = html_path.read_text(encoding="utf-8")
    asyncio.run(
        send_email(
            recipient="weitkicker145@gmail.com",
            subject="Подтверждение регистрации на Kload",
            plain_content="Здравствуйте! Подтвердите свою регистрацию, перейдя по ссылке в письме.",
            html_content=html_content,
        )
    )
    return "Письмо отправлено успешно"