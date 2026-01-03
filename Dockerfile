# Base image
FROM ubuntu:24.04

# System dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    python3 \
    python3-pip \
    bash \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install multiprocessing-logging

# Install Scarb via starkup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.starkup.dev | bash

# Add starkup tools to PATH
ENV PATH="/root/.starkup/bin:${PATH}"

# Set working directory
WORKDIR /Kairox

# Copy project
COPY . /Kairox

# Default shell
CMD ["/bin/bash"]
