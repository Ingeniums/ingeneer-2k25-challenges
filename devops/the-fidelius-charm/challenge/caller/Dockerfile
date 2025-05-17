FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir requests cryptography

COPY script.py .
COPY story.md .

RUN mkdir -p /var/logs

CMD ["python", "script.py"]
