FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    ca-certificates \
    openssl \
    openssh-client \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    expect \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic link for python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install BOSH CLI
RUN wget -O /usr/local/bin/bosh https://github.com/cloudfoundry/bosh-cli/releases/download/v7.8.2/bosh-cli-7.8.2-linux-amd64 \
    && chmod +x /usr/local/bin/bosh

# Install uv (Astral's Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

# Verify installations
RUN bosh --version && \
    openssl version && \
    python --version 
#    uv --version

# Default command
CMD ["/bin/bash"]
