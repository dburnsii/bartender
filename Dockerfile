FROM debian:bullseye

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python3-pip python3-venv wget gcc \
                       libsystemd-dev npm build-essential

ENV CC=arm-linux-gnueabihf-gcc
ENV CXX=arm-linux-gnueabihf-g++

WORKDIR /home/bartender

CMD ["/usr/bin/make", "deb"]
