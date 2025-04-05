FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]