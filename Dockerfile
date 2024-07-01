# Use the official Ubuntu 22.04 LTS base image
FROM ubuntu:22.04 as stacks2

RUN apt-get update && apt-get install -y \
    wget \
    g++ \
    zlib1g-dev \
    make \
    python3 \
&& rm -rf /var/lib/apt/lists/*

RUN wget https://catchenlab.life.illinois.edu/stacks/source/stacks-2.66.tar.gz

RUN tar xfvz stacks-2.66.tar.gz && \
    cd stacks-2.66 && \
    ./configure && \
    make && \
    make install && \
    cd .. && rm -rf stacks-2.66 stacks-2.66.tar.gz

RUN denovo_map.pl -v || exit 0

COPY parameter_optimization.py /

RUN chmod +x parameter_optimization.py
