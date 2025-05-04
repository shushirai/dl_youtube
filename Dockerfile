FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    locales \
    sudo \
    wget \
    vim \
    python3 \
    python3-pip \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ユーザー作成
RUN useradd -m -u 1000 -s /bin/bash shu_docker && \
    echo 'shu_docker ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER shu_docker
WORKDIR /home/shu_docker/ws

COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt

CMD ["/bin/bash"]
