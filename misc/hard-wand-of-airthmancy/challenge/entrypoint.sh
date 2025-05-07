#!/bin/sh

EXEC="./server.py"
PORT=4000

socat -dd -T300 tcp-l:$PORT,reuseaddr,fork,keepalive exec:"python3 $EXEC"