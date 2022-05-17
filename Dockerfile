FROM python:3.8-alpine

RUN apk add --no-cache tzdata git

RUN apk upgrade -U \
    && apk add --no-cache -u ca-certificates libffi-dev libva-intel-driver supervisor python3-dev build-base linux-headers pcre-dev curl busybox-extras \
    && rm -rf /tmp/* /var/cache/*

COPY requirements.txt /
COPY lib/requirements.txt /lib/requirements.txt
RUN pip --no-cache-dir install --upgrade pip setuptools
RUN pip --no-cache-dir install -r /lib/requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

COPY conf/supervisor/ /etc/supervisor.d/
COPY . /webapps

WORKDIR /webapps
