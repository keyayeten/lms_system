# lms_system


# Локальный запуск:
- Перед запуском необходмо поместить в каждый модуль переменные окружения .env

- - Пример для основной директории:
```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=lmsdb
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
```
- - Пример для web:
```
DB_URL="postgresql+asyncpg://user:password@db:5432/lmsdb"
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=lmsdb
RABBIT_URL="amqp://guest:guest@rabbitmq:5672/"
RABBIT_HOST=rabbitmq
RABBIT_PORT=5672
```
- - Пример для content_parser:
```
DB_URL="postgresql+asyncpg://user:password@db:5432/lmsdb"
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=lmsdb
RABBIT_URL="amqp://guest:guest@rabbitmq:5672/"
RABBIT_HOST=rabbitmq
RABBIT_PORT=5672
```
- Запуск осуществляется командой ```docker-compose up --build -d```

- При успешном запуске проверьте логи контейнеров.

- - Контейнер robyn_app, пример логов при успешном запуске:
```
2025-04-06 18:22:36 INFO:robyn.logger:Database connected and initialized successfully.
2025-04-06 18:22:40 INFO:robyn.logger:RabbitMQ connected successfully.
...
2025-04-06 18:22:36 2025-04-06 15:22:36,579 INFO sqlalchemy.engine.Engine [no key 0.00012s] ()
2025-04-06 18:22:36 2025-04-06 15:22:36,581 INFO sqlalchemy.engine.Engine CREATE INDEX ix_users_id ON users (id)
2025-04-06 18:22:36 2025-04-06 15:22:36,581 INFO sqlalchemy.engine.Engine [no key 0.00009s] ()
2025-04-06 18:22:36 2025-04-06 15:22:36,584 INFO sqlalchemy.engine.Engine COMMI
```
- - Контейнер content_parser, пример логов при успешном запуске:
```
2025-04-06 18:22:41 ✅ Database connection successful
2025-04-06 18:22:41 2025-04-06 15:22:41,600 INFO     -      | test |            - `BaseHandler` waiting for messages
2025-04-06 18:22:33 2025-04-06 15:22:33,549 INFO     - FastStream app starting...
2025-04-06 18:22:41 2025-04-06 15:22:41,603 INFO     - FastStream app started successfully! To exit, press CTRL+C
```