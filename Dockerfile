# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y build-essential libpq-dev curl

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

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
