FROM jamiehewland/alpine-pypy@sha256:7520e252684f76bd393c85538e492c86e06c097da40c595e688b036e9d2ca34a as TESTER
MAINTAINER @ashmastaflash

RUN apk add -U \
    curl \
    expect \
    gzip \
    tcl \
    unzip

RUN pip install \
    opencellid==1.2 \
    psutil \
    python-dateutil==2.6.0 \
    pytest \
    pytest-cov \
    pytest-profiling \
    requests==2.13.0 \
    twilio==5.7.0

COPY sitch/ /app/sitch


WORKDIR /app/sitch

RUN /usr/local/bin/pypy -mpy.test \
    --cov=sitchlib \
    --cov-report term-missing \
    --profile \
    /app/sitch/test

##################

FROM jamiehewland/alpine-pypy@sha256:7520e252684f76bd393c85538e492c86e06c097da40c595e688b036e9d2ca34a
MAINTAINER @ashmastaflash

RUN apk add -U \
    curl \
    expect \
    gzip \
    tcl \
    unzip


RUN pip install \
    opencellid==1.2 \
    psutil \
    python-dateutil==2.6.0 \
    requests==2.13.0 \
    twilio==5.7.0

COPY sitch/ /app/sitch


WORKDIR /app/sitch

ENTRYPOINT ["/usr/local/bin/pypy"]
CMD ["/app/sitch/runner.py"]
