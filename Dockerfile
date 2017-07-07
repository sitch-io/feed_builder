FROM jamiehewland/alpine-pypy:2

RUN apk update && apk add \
    gcc \
    linux-headers \
    musl-dev

RUN pip install \
    opencellid==1.2 \
    psutil \
    requests==2.13.0 \
    twilio==5.7.0

COPY sitch/ /app/sitch


WORKDIR /app/sitch

CMD ["/usr/local/bin/pypy", "/app/sitch/runner.py"]
