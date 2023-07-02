# First stage: Node.js build
FROM node:18.16.1-bullseye as builder

ENV DEBIAN_FRONTEND=noninteractive
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /app

COPY . .

RUN cd view/minutes-maker \
    && cp /app/.env . \
    && npm install \
    && npm run build

# Second stage: Python backend
FROM python:3.11.4-slim-bullseye as backend

ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1

WORKDIR /app

RUN apt update && apt install -y software-properties-common curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/src /app/src
COPY --from=builder /app/main.py /app/main.py
COPY --from=builder /app/requirements.lock /app/requirements.lock
COPY --from=builder /app/pyproject.toml /app/pyproject.toml
COPY --from=builder /app/README.md /app/README.md

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3 \
    && python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python3 -m pip install --no-cache-dir -r requirements.lock

# Third stage: Nginx for static files
FROM nginx:latest as frontend

ENV DEBIAN_FRONTEND=noninteractive

COPY --from=builder /app/view/minutes-maker/build /usr/share/nginx/html
