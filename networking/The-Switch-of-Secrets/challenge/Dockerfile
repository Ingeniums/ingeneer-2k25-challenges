FROM alpine:3.16

# Install socat and bash
RUN apk update && apk add --no-cache socat bash

# Copy the challenge script into the container
COPY shell.sh /challenge.sh
RUN chmod +x /challenge.sh

# Expose port 1234
EXPOSE 1234

# Use socat to listen on port 1234 and execute challenge.sh for each connection
CMD ["socat", "TCP-LISTEN:1234,reuseaddr,fork", "EXEC:/challenge.sh,pty,stderr,setsid,sigint,sane"]
