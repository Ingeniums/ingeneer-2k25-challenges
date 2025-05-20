# sudo docker build -t asd .
# sudo docker run -d -p 1337:1337 --rm -it asd

FROM ubuntu:22.04


RUN apt-get update

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY rev .
COPY flag.txt .
COPY wrapper.sh .
COPY ynetd .

RUN chown -R ctf:ctf /home/ctf
EXPOSE 1337

USER ctf
RUN chmod +x ynetd wrapper.sh rev 
CMD ./ynetd -p 1337 ./wrapper.sh