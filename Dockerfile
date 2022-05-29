# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

# install git
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt \
    && python -m pip install git+https://github.com/yashenkoxciv/imagenet-viewer.git

CMD python app.py
