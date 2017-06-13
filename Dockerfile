FROM alpine:3.4
MAINTAINER ash.d.wilson@gmail.com

RUN apk update && apk add \
    gcc \
    linux-headers \
    musl-dev \
    python \
    python-dev

ADD https://bootstrap.pypa.io/get-pip.py /
RUN python /get-pip.py

RUN pip install \
    opencellid==1.2 \
    psutil \
    requests==2.13.0 \
    twilio==5.7.0

COPY sitch/ /app/sitch


WORKDIR /app/sitch

CMD ["/usr/bin/python", "/app/sitch/runner.py"]
