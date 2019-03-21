FROM jamiehewland/alpine-pypy@sha256:7520e252684f76bd393c85538e492c86e06c097da40c595e688b036e9d2ca34a as TESTER
MAINTAINER @ashmastaflash

RUN apk add -U \
    curl \
    expect \
    gzip \
    tcl \
    unzip

COPY requirements* /

RUN pip install -r requirements-test.txt

COPY sitch/ /app/sitch


WORKDIR /app/sitch

RUN ls /app/sitch

RUN /usr/local/bin/pypy -mpy.test \
    --cov=sitchlib \
    --cov-report term-missing \
    --profile \
    ./

##################

FROM jamiehewland/alpine-pypy@sha256:7520e252684f76bd393c85538e492c86e06c097da40c595e688b036e9d2ca34a
MAINTAINER @ashmastaflash

RUN apk add -U \
    curl \
    expect \
    gzip \
    tcl \
    unzip

COPY requirements* /

RUN pip install -r requirements.txt

COPY sitch/ /app/sitch


WORKDIR /app/sitch

ENTRYPOINT ["/usr/local/bin/pypy"]
CMD ["/app/sitch/runner.py"]
