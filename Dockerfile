FROM debian:buster-slim

ARG python_version=3.8.2
ENV PYTHON_VERSION ${python_version}

RUN apt update && \
    apt -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -O https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz

RUN tar -xf Python-${PYTHON_VERSION}.tar.xz

WORKDIR /Python-${PYTHON_VERSION}

RUN ./configure --enable-optimizations

RUN make -j 4

RUN make altinstall

RUN python3.8 -m pip install prometheus_client jira

COPY collector.py /entrypoint.py

CMD ["/entrypoint.py"]
ENTRYPOINT ["python3.8"]