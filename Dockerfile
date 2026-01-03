# Base image
FROM ubuntu:24.04

# 1. Combined System Dependencies (One layer to save 'apt update' time)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    bash \
    ca-certificates \
    tar \
    && rm -rf /var/lib/apt/lists/*

# 2. Python Virtual Environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir multiprocessing-logging

# 3. Direct Scarb Installation (The "Fast" Way)
# This replaces the slow starkup script. 
RUN SCARB_VERSION=2.13.1 && \
    curl -L "https://github.com/software-mansion/scarb/releases/download/v${SCARB_VERSION}/scarb-v${SCARB_VERSION}-x86_64-unknown-linux-musl.tar.gz" -o scarb.tar.gz && \
    tar -xvf scarb.tar.gz && \
    mv scarb-v${SCARB_VERSION}-x86_64-unknown-linux-musl/bin/scarb /usr/local/bin/scarb && \
    rm -rf scarb.tar.gz scarb-v${SCARB_VERSION}-x86_64-unknown-linux-musl

# Set working directory
WORKDIR /Kairox

# Copy project (do this last so code changes don't break the build cache)
COPY . /Kairox

# Verify installation during build
RUN scarb --version

CMD ["/bin/bash"]