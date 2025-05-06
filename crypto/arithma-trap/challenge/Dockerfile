
FROM python:3.10-slim
WORKDIR /app
COPY FLAG.py .
COPY server.py .
COPY entrypoint.sh .
RUN chmod +x server.py
RUN chmod +x entrypoint.sh
RUN apt update && apt upgrade -y && apt install -y ncat socat
RUN pip install pycryptodome
EXPOSE 4000
CMD ["nc","-lv","4000","-e","./server.py"]
ENTRYPOINT ["./entrypoint.sh"]
