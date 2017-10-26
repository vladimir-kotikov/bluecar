# This is based on https://github.com/resin-io-projects/boombeastic/pull/34/files

# Don't use stretch as it doesn't have properly patched bluez yet
# See https://github.com/raspberrypi/linux/issues/1314#issuecomment-190784653
FROM resin/raspberrypi3-debian:jessie

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    # TODO: instead pi-bluetooth install just raspberrypi-sys-mods and
    # craft own hci configuration service (+ device name setup)
    bluez bluez-firmware pi-bluetooth socat

RUN echo deb http://deb.debian.org/debian buster main >> /etc/apt/sources.list.d/buster-main.list && \
    apt-get update && \
    apt-get install -yq --no-install-recommends -t buster \
    pulseaudio pulseaudio-module-bluetooth


COPY conf/pulseaudio-bluetooth.conf /etc/dbus-1/system/
# TODO: Ideally DB should reconnect to last device automatically
COPY conf/bluetooth-main.conf /etc/bluetooth/main.conf

RUN echo "resample-method = ffmpeg" >> /etc/pulse/daemon.conf
RUN echo "avoid-resampling = yes" >> /etc/pulse/daemon.conf
RUN echo "load-module module-switch-on-connect" >> /etc/pulse/system.pa
RUN echo "load-module module-bluetooth-discover" >> /etc/pulse/system.pa
RUN echo "load-module module-bluetooth-policy" >> /etc/pulse/system.pa
RUN sed 's/^load-module module-console-kit/#load-module module-console-kit/' -i /etc/pulse/system.pa
RUN sed 's/^load-module module-udev-detect/load-module module-udev-detect tsched=0/' -i /etc/pulse/system.pa

## Services

COPY service/hciuart.service /lib/systemd/system/
COPY service/socat.service /etc/systemd/system/basic.target.wants/

# Run bluetooth service in debug mode
RUN sed 's/^ExecStart=\/usr\/lib\/bluetooth\/bluetoothd/ExecStart=\/usr\/lib\/bluetooth\/bluetoothd -d/' \
    -i /lib/systemd/system/bluetooth.service

# hciattach searches for firmware in /etc/firmware instead of /lib/firmware
RUN ln -s /lib/firmware/brcm /etc/firmware

RUN adduser root pulse-access && adduser pulse bluetooth && adduser root bluetooth
RUN echo ForwardToConsole=yes >> /etc/systemd/journald.conf

ENV DISPLAY :0
ENV INITSYSTEM on
EXPOSE 7272:7272
CMD ["/usr/bin/pulseaudio", "--system", "--verbose", "--disallow-exit", "--disable-shm", "--exit-idle-time=-1"]
