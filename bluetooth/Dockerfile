# This is based on https://github.com/resin-io-projects/boombeastic/pull/34/files

# Don't use stretch as it doesn't have properly patched bluez yet
# See https://github.com/raspberrypi/linux/issues/1314#issuecomment-190784653
FROM resin/raspberrypi3-debian

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    # pi-bluetooth is required to activate HCI interface
    # TODO: instead pi-bluetooth install just raspberrypi-sys-mods and
    # craft own hci configuration service (+ device name setup)
    # TODO: hciuart service sometimes still fail to flash firmware due to timeout
    #   Custom service shoud use https://www.freedesktop.org/software/systemd/man/systemd.service.html#Restart=
    # to restart service when attach fails
    bluez bluez-firmware pulseaudio pulseaudio-module-bluetooth pi-bluetooth socat

# TODO: Remove lines below - these are only for testing purposes
RUN apt-get install -yq --no-install-recommends mpg123
COPY ./BlueZedEx.mp3 /

COPY conf/alsa-base.conf /etc/modprobe.d/
COPY conf/pulseaudio-bluetooth.conf /etc/dbus-1/system/
# TODO: Ideally DB should reconnect to last device automatically
COPY conf/bluetooth-main.conf /etc/bluetooth/main.conf

RUN echo "resample-method = ffmpeg" >> /etc/pulse/daemon.conf
# TODO: build pulseaudio from sources to enable this
# RUN echo "avoid-resampling = yes" > /etc/pulse/daemon.conf
RUN echo "load-module module-switch-on-connect" >> /etc/pulse/system.pa
RUN echo "load-module module-bluetooth-discover" >> /etc/pulse/system.pa
RUN echo "load-module module-bluetooth-policy" >> /etc/pulse/system.pa
RUN sed 's/^load-module module-console-kit/#load-module module-console-kit/' -i /etc/pulse/system.pa
RUN sed 's/^load-module module-udev-detect/load-module module-udev-detect tsched=0/' -i /etc/pulse/system.pa

COPY service/socat.service /etc/systemd/system/basic.target.wants/
# hciattach searches for firmware in /etc/firmware instead of /lib/firmware
RUN ln -s /lib/firmware/brcm /etc/firmware

RUN adduser root pulse-access

ENV DISPLAY :0
ENV INITSYSTEM on
EXPOSE 7272:7272
CMD ["/usr/bin/pulseaudio", "--system", "--verbose", "--disallow-exit", "--disable-shm", "--exit-idle-time=-1"]
