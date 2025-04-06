FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY web/requirements.txt web/requirements.txt
RUN pip install --no-cache-dir -r web/requirements.txt

ENV PYTHONPATH="/app/"
ENV APP_DIR="/app/web/"
ENV APP_BIN="${APP_DIR}app.py"

COPY web web
COPY utils utils


EXPOSE 8080

CMD python ${APP_BIN}