FROM php:8-fpm-alpine3.20

WORKDIR /app
COPY src/ .

RUN addgroup -S ctfplayer && adduser -S ctfplayer -G ctfplayer
RUN chown -R ctfplayer:ctfplayer /app

USER ctfplayer
EXPOSE 8080

CMD ["php", "-S", "0.0.0.0:8080"]
