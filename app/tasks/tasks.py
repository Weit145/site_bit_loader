import asyncio
from pathlib import Path

from jinja2 import Template

from app.tasks.celery import app
from app.tasks.email.email import send_email


@app.task(name="send_email")
def send_message(token:str, username:str,email:str):
    html_path = Path("app/templates/pod_reg.html")
    html_content = html_path.read_text(encoding="utf-8")

    template = Template(html_content)
    rendered_html = template.render(
        confirm_url=f"http://127.0.0.1:8000/users/confirm/?token_pod={token}",
        username=username,
        site_url="http://localhost:5173/",
        support_email="support@kload.com",
        unsubscribe_url="http://127.0.0.1:8000/unsubscribe",
        year=2025
    )
    asyncio.run(
        send_email(
            recipient=email,
            subject="Подтверждение регистрации на Kload",
            plain_content="Здравствуйте! Подтвердите свою регистрацию, перейдя по ссылке в письме.",
            html_content=rendered_html,
        )
    )
    return "Письмо отправлено успешно"
