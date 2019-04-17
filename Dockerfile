FROM pypy:3.6 as TESTER

RUN apt-get update && apt-get install -y \
    curl \
    expect \
    gzip \
    tcl \
    unzip

COPY requirements* /

RUN pip install --no-cache-dir -r requirements-test.txt

COPY sitch/ /app/sitch

WORKDIR /app/sitch

RUN ls /app/sitch

RUN pypy3 -m pytest \
    --cov=sitchlib \
    --cov-report term-missing \
    --profile \
    ./

##################

FROM pypy:3.6

RUN apt-get update && apt-get install -y \
    curl \
    expect \
    gzip \
    tcl \
    unzip

COPY requirements* /

RUN pip install --no-cache-dir -r requirements.txt

COPY sitch/ /app/sitch

WORKDIR /app/sitch

ENTRYPOINT ["pypy3"]
CMD ["/app/sitch/runner.py"]
