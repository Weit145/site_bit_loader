from app.tasks.celery import app

@app.task(name="app.tasks.send_email.send_message")
def send_message():
    print("✅ send_message выполнена")
    return "Hello World"
