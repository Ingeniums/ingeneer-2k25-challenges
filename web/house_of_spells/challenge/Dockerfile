FROM python:slim
WORKDIR /app
COPY challenge/ ./
COPY requirements.txt ./
COPY flag.txt /
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3","app.py"]