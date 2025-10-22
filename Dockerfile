# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential libpq-dev curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*
# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry==1.8.3

# Создаём директорию приложения
WORKDIR /app

# Копируем файлы проекта
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости без dev-зависимостей
RUN poetry install --no-root --without dev


# Копируем исходники
COPY . .

# Указываем порт (FastAPI обычно слушает 8000)
EXPOSE 8000

# Команда запуска через Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
