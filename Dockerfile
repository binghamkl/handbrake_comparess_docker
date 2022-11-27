# syntax=docker/dockerfile:1

# FROM python:3.11-slim-buster
## RUN flatpak --user install https://flathub.org/repo/appstream/fr.handbrake.ghb.flatpakref

FROM alpine:edge
RUN apk update && apk add --no-cache handbrake --repository="http://dl-cdn.alpinelinux.org/alpine/edge/testing"

RUN apk update
RUN apk add --no-cache python3 py3-pip
# RUN apk install python

WORKDIR /app

# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt

COPY app .

CMD [ "python", "handbrake.py"]