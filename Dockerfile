FROM debian:bullseye

# Install build packages
RUN apt-get update && apt-get -y upgrade
RUN apt-get install --no-install-recommends -y python3 python3-pip \
                       python3-venv wget curl gcc g++ python3-dev \
                       libsystemd-dev systemd make dpkg-sig \
                       && rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get install --no-install-recommends -y python3-apt

RUN pip3 install -U pip setuptools

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt install -y nodejs

RUN npm -g install react-scripts

RUN useradd bartender

WORKDIR /home/bartender

CMD ["/usr/bin/make", "deb_signed"]
