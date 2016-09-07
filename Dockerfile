FROM ubuntu:16.04
MAINTAINER ash.d.wilson@gmail.com

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
    python \
    python-pip

RUN pip install \
    requests \
    twilio

COPY sitch/ /app/sitch

WORKDIR /app/sitch
CMD ["/usr/bin/python", "/app/sitch/runner.py"]
