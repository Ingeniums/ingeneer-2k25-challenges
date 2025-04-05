FROM alpine:3.14

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /app

COPY ./Dockerfile .

RUN mkdir /scripts
COPY ./script.py /bin/script.py

RUN mkdir -p /var/log/internal/uploads/
ENV UPLOADS_PATH=/var/log/internal/uploads
COPY ./files/* /var/log/internal/uploads/
COPY ./flag.txt /flag.txt

ENTRYPOINT [ "python", "-u", "/bin/script.py" ]
