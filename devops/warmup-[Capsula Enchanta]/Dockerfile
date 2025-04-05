FROM python:3

WORKDIR /app

COPY ./Dockerfile .

RUN mkdir /scripts
COPY ./script.py /bin/script.py

RUN mkdir -p /var/log/internal/uploads/
ENV UPLOADS_PATH=/var/log/internal/uploads
COPY ./files/* /var/log/internal/uploads/
COPY ./flag.txt /flag.txt

ENTRYPOINT [ "python", "-u", "/bin/script.py" ]
