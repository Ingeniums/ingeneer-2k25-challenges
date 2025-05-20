FROM python:3.10-slim
WORKDIR /app
COPY ./challenge/server.py .
COPY entrypoint.sh .
COPY flag.txt /flag.txt
RUN chmod +x server.py \
    && chmod +x entrypoint.sh \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y socat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
EXPOSE 4000
ENTRYPOINT ["./entrypoint.sh"]