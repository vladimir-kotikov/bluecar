FROM arm32v7/debian:stretch-slim

ENV LC_ALL C.UTF-8
ENV DEBIAN_FRONTEND noninteractive

COPY 01_nodoc /etc/dpkg/dpkg.cfg.d/
COPY 01_buildconfig /etc/apt/apt.conf.d/

# We only want few core services run in the container.
RUN find /etc/systemd/system \
    /lib/systemd/system \
    -path '*.wants/*' \
    -not -name '*journald*' \
    -not -name '*udevd*' \
    -not -name '*systemd-tmpfiles*' \
    -not -name '*systemd-user-sessions*' \
    -exec rm \{} \;

RUN apt-get update && apt-get install apt-utils
RUN apt-get upgrade && apt-get install bluez pulseaudio

## Authorize users (each user that will be using PA must belong to group pulse-access)
RUN adduser $(whoami) pulse-access

# Authorize PulseAudio - which will run as user pulse - to use BlueZ D-BUS interface:
ADD bootstrap/pulseaudio-bluetooth.conf /etc/dbus-1/system.d/

# Make USB sound preferred over analog
ADD bootstrap/alsa-base.conf /etc/modprobe.d/

# Configure pulseaudio - change "resample-method"
RUN echo "resample-method = ffmpeg" > /etc/pulse/daemon.conf
# Available on PA11 only. See https://www.freedesktop.org/wiki/Software/PulseAudio/Notes/11.0/
# RUN echo "avoid-resampling = yes" > /etc/pulse/daemon.conf

# Load  Bluetooth discover and policy modules in SYSTEM MODE
# See https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/#index36h3
ADD bootstrap/system.pa /bootstrap/
RUN cat /bootstrap/system.pa >> /etc/pulse/system.pa

# Create and start a systemd service for running pulseaudio in System Mode as user "pulse".
ADD bootstrap/pulseaudio.service /bootstrap/
RUN cat /bootstrap/pulseaudio.service >> /etc/systemd/system/pulseaudio.service

RUN systemctl enable pulseaudio.service
# RUN systemctl daemon-reload && systemctl enable pulseaudio.service

# Set usb audio card as default
ADD bootstrap/pulseaudio-default-sink.sh /bootstrap/
RUN . /bootstrap/pulseaudio-default-sink.sh
