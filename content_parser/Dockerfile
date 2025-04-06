FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY content_parser/requirements.txt content_parser/requirements.txt
RUN pip install --no-cache-dir -r content_parser/requirements.txt

ENV PYTHONPATH="/app/"
ENV APP_DIR="/app/content_parser/"
ENV APP_BIN="${APP_DIR}app.py"

COPY content_parser content_parser
COPY utils utils

CMD faststream run content_parser.app:app