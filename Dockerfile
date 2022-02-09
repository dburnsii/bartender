FROM debian:bullseye

RUN apt-get update
RUN apt-get install --no-install-recommends -y python3 python3-pip \
                       python3-venv wget gcc g++ python3-dev \
                       libsystemd-dev systemd npm make \
                       && rm -rf /var/lib/apt/lists/*

ENV CC=arm-linux-gnueabihf-gcc
ENV CXX=arm-linux-gnueabihf-g++

WORKDIR /home/bartender

CMD ["/usr/bin/make", "deb"]
