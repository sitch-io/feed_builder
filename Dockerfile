FROM alpine:3.4
MAINTAINER ash.d.wilson@gmail.com

RUN apk update && \
    apk add \
    python

ADD https://bootstrap.pypa.io/get-pip.py /
RUN python /get-pip.py

RUN pip install \
    requests \
    twilio

COPY sitch/ /app/sitch


WORKDIR /app/sitch

CMD ["/usr/bin/python", "/app/sitch/runner.py"]
