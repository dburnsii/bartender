FROM debian:bullseye

RUN apt update && apt upgrade -y
RUN apt install -y python3 python3-pip python3-venv wget gcc dh-systemd libsystemd-dev npm

ENV CC=arm-linux-gnueabihf-gcc
ENV CXX=arm-linux-gnueabihf-g++

WORKDIR /home/bartender
