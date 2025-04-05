FROM alpine:3.14

WORKDIR /app

COPY ./Dockerfile .

RUN mkdir /scripts
COPY ./script.py /script

RUN mkdir -p /var/util/internal/uploads/
ENV UPLOADS_PATH=/var/util/internal/uploads/
RUN cp -r ./files/* /var/util/internal/uploads/
RUN cp ./flag.txt /flag.txt

ENTRYPOINT [ "python", "/scripts/script.py" ]
