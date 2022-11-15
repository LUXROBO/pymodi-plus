FROM python:3.10-slim-buster
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN python setup.py install --user
WORKDIR /workspace

LABEL org.opencontainers.image.source="https://github.com/luxrobo/pymodi-plus"
