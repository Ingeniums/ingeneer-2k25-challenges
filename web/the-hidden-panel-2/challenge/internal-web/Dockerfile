FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install -r /app/requirements.txt

RUN useradd -m flaskuser

RUN chmod 700 /app && chmod 600 /app/flag.txt

RUN chown -R flaskuser:flaskuser /app

USER flaskuser

CMD ["python", "app.py"]
