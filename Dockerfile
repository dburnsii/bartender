FROM debian:bullseye

RUN apt-get update
RUN apt-get install --no-install-recommends -y python3 python3-pip \
                       python3-venv wget gcc g++ python3-dev \
                       libsystemd-dev systemd npm make dpkg-sig \
                       && rm -rf /var/lib/apt/lists/*

RUN pip3 install -U pip setuptools

WORKDIR /home/bartender

CMD ["/usr/bin/make", "deb_signed"]
