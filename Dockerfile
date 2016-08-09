FROM django:1.9.8-python3
MAINTAINER Maru Berezin

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get remove --purge -y gcc \
    && apt-get autoremove -y && apt-get autoclean \
    && rm -rf /tmp/* /var/tmp/* && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm requirements.txt
