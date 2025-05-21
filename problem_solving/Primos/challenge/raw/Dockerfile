FROM alpine:3.16

# Install Python3, py3-pip, socat, and bash
RUN apk update && apk add --no-cache python3 py3-pip socat bash

# Copy the Python challenge file into the container
COPY challenge.py /challenge.py
RUN chmod +x /challenge.py

# Expose port 6245
EXPOSE 6245

# Run the Python challenge on each connection via socat
CMD ["socat", "TCP-LISTEN:6245,reuseaddr,fork", "EXEC:'python3 /challenge.py',pty,stderr,setsid,sigint,sane"]
