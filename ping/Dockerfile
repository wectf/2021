FROM ubuntu:18.04
RUN apt update
ARG DEBIAN_FRONTEND=noninteractive

RUN apt install -y redis-server python3-pip nodejs npm tcpdump libpcap0.8-dev


RUN mkdir /app
WORKDIR /app

# Python stuffs
RUN pip3 install redis scapy getmac netifaces
COPY main.py /app/main.py
COPY config.py /app/config.py
COPY net.py /app/net.py
COPY recv.py /app/recv.py
COPY utils.py /app/utils.py

# Node stuffs
COPY app.js /app/app.js
COPY index.js /app/index.js
COPY package.json /app/package.json
COPY views /app/views
COPY bin /app/bin
RUN npm i

COPY start.sh /app/start.sh

RUN echo "we{e71dd162-6233-41de-affa-076d5463c6f7@r3d1s_cAn_b3_acCe33ed_v1a_P1ng}" > /flag.txt
RUN chmod +x ./start.sh

EXPOSE 3000

USER root
CMD timeout 5m ./start.sh
