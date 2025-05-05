FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir Flask cryptography

COPY decrypt_script.py /tmp/decrypt_script.py

RUN chmod +x /tmp/decrypt_script.py && rm /tmp/decrypt_script.py

COPY server.py .
COPY server-help.md .
COPY decrypt-help.md .

RUN mkdir -p /var/logs

EXPOSE 8000

CMD ["python", "server.py"]
