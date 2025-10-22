from app.tasks.celery import app
import asyncio

from app.tasks.email.email import send_email

# @app.task(name="app.tasks.send_email.send_message")
# def send_message():
#     print("✅ send_message выполнена")
#     return "Hello World"



@app.task(name="send_email")
def send_message():
    asyncio.run(
        send_email(
            recipient="kocnevs.jk@yandex.ru",
            subject="Рыжий лох",
            plain_content="xd",
            html_content="<h3>Вопросы?</h3><p>А<b>А</b>А<i>А</i>?</p>",
        )
    )
    return "Письмо отправлено успешно"