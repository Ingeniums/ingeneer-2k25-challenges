FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    iputils-ping \
    openssh-server \
    net-tools \
    coreutils \
    --no-install-recommends && \
    apt-get remove --purge -y \
    gcc g++ make perl python3 python2 vim nano man-db info less && \
    apt-get autoremove -y && apt-get clean && \
    rm -rf /usr/share/man /usr/share/doc /usr/share/locale /var/cache/*

RUN useradd -ms /bin/rbash ctfplayer && echo 'ctfplayer:ctfpassword' | chpasswd

RUN mkdir /home/ctfplayer/bin && \
    ln -s /bin/cat /home/ctfplayer/bin/cat && ln -s /bin/ls /home/ctfplayer/bin/ls && ln -s /sbin/ifconfig /home/ctfplayer/bin/ifconfig  && ln -s /bin/ping /home/ctfplayer/bin/ping && \
    chown -R ctfplayer:ctfplayer /home/ctfplayer && \
    echo 'export PATH=$HOME/bin' >> /home/ctfplayer/.bashrc && \
    echo 'readonly PATH' >> /home/ctfplayer/.bashrc

# SSH setup
RUN mkdir /var/run/sshd
COPY sshd_config /etc/ssh/sshd_config
COPY fake_flag.txt /home/ctfplayer/.flag.txt
RUN chown ctfplayer:ctfplayer /home/ctfplayer/.flag.txt

CMD ["/usr/sbin/sshd", "-D"]
