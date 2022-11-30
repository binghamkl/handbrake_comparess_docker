# syntax=docker/dockerfile:1

#FROM python:3.11-slim-buster
## RUN flatpak --user install https://flathub.org/repo/appstream/fr.handbrake.ghb.flatpakref

#RUN apt-get update
#RUN apt-get -y install appstream autoconf automake autopoint build-essential cmake git libass-dev libbz2-dev libfontconfig1-dev libfreetype6-dev libfribidi-dev libharfbuzz-dev libjansson-dev liblzma-dev libmp3lame-dev libnuma-dev libogg-dev libopus-dev libsamplerate-dev libspeex-dev libtheora-dev libtool libtool-bin libturbojpeg0-dev libvorbis-dev libx264-dev libxml2-dev libvpx-dev m4 make meson nasm ninja-build patch pkg-config python tar zlib1g-dev
#RUN apt-get -y install libva-dev libdrm-dev
#RUN apt-get -y install intltool libdbus-glib-1-dev libglib2.0-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk-3-dev libgudev-1.0-dev libnotify-dev libwebkit2gtk-4.0-dev
#RUN apt-get update
#RUN apt-get -y remove cmake
#RUN pip install cmake --upgrade
##RUN git clone https://github.com/HandBrake/HandBrake.git && cd HandBrake
#WORKDIR /HandBrake

#RUN git tag --list | grep ^1\.2\.
#RUN git checkout refs/tags/$(git tag -l | grep -E '^1\.2\.[0-9]+$' | tail -n 1)
#RUN ./configure --launch-jobs=$(nproc) --launch --enable-qsv --disable-gtk
#RUN make --directory=build install

FROM alpine:edge
RUN apk update && apk add --no-cache handbrake --repository="http://dl-cdn.alpinelinux.org/alpine/edge/testing"

#FROM jlesage/handbrake
RUN apk update
# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN apk update && apk add tzdata
ENV TZ="America/New_York"

WORKDIR /app

# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt

COPY app .

CMD [ "python", "handbrake.py"]