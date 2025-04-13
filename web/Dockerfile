FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости Python
COPY ./web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Альтернативно, можно использовать psycopg2-binary вместо psycopg2
# RUN sed -i 's/psycopg2/psycopg2-binary/' requirements.txt && \
#     pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменные окружения
ENV PYTHONPATH="/app"
ENV APP_MODULE="web.app:app"
ENV APP_HOST="0.0.0.0"
ENV APP_PORT=8080

# Копируем исходный код
COPY ./web ./web
COPY ./utils ./utils

# Открываем порт
EXPOSE ${APP_PORT}

# Запускаем приложение с помощью uvicorn
CMD uvicorn --host ${APP_HOST} --port ${APP_PORT} ${APP_MODULE}