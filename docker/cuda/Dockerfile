FROM node:18.16.1-bullseye as builder

ENV DEBIAN_FRONTEND=noninteractive
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /app

# Copy the current directory into the container
COPY . .

# install react dependencies and build
RUN cd view/minutes-maker \
    && cp /app/.env . \
    && npm install \
    && npm run build

FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 as backend

ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1

WORKDIR /app

RUN apt update && apt install -y software-properties-common curl \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt update \
    && apt install -y --no-install-recommends python3.11-dev ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN echo "export PATH=/usr/local/cuda/bin:$PATH" >> /etc/bash.bashrc \
    && echo "export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH" >> /etc/bash.bashrc

COPY --from=builder /app/src /app/src
COPY --from=builder /app/main.py /app/main.py
COPY --from=builder /app/requirements.lock /app/requirements.lock
COPY --from=builder /app/pyproject.toml /app/pyproject.toml
COPY --from=builder /app/README.md /app/README.md

# install python dependencies
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 \
    && python3.11 -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python3.11 -m pip install --no-cache-dir -r requirements.lock

FROM nginx:latest as frontend

ENV DEBIAN_FRONTEND=noninteractive

COPY --from=builder /app/view/minutes-maker/build /usr/share/nginx/html
