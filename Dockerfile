# Use the official Ubuntu 22.04 LTS base image
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    wget \
    g++ \
    zlib1g-dev

RUN wget https://catchenlab.life.illinois.edu/stacks/source/stacks-2.66.tar.gz

RUN tar xfvz stacks-2.xx.tar.gz && \
    cd stacks-2.66 && \
    ./configure && \
    make && make install