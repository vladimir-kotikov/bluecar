FROM resin/raspberrypi3-debian:stretch

RUN echo deb http://archive.raspberrypi.org/debian/ stretch main ui >> /etc/apt/sources.list.d/raspi.list && \
    echo deb http://deb.debian.org/debian buster main >> /etc/apt/sources.list.d/buster.list && \
    apt-key adv --keyserver pgp.mit.edu  --recv-key 0x82B129927FA3303E && \
    apt-get update && \
    apt-get install -y -t stretch bluez socat && \
    apt-get install -y pulseaudio pulseaudio-module-bluetooth ofono


COPY conf/pulseaudio-bluetooth.conf /etc/dbus-1/system/

# TODO: Backup ofono's configuration file
COPY conf/ofono.conf /etc/dbus-1/system.d/

# TODO: Ideally DB should reconnect to last device automatically
RUN cp /etc/bluetooth/main.conf /etc/bluetooth/main.conf.old
COPY conf/bluetooth-main.conf /etc/bluetooth/main.conf

RUN echo "resample-method = ffmpeg" >> /etc/pulse/daemon.conf && \
    echo "avoid-resampling = yes" >> /etc/pulse/daemon.conf && \
    echo "load-module module-switch-on-connect" >> /etc/pulse/system.pa && \
    echo "load-module module-bluetooth-discover headset=ofono" >> /etc/pulse/system.pa && \
    echo "load-module module-bluetooth-policy" >> /etc/pulse/system.pa && \
    sed 's/^load-module module-udev-detect/load-module module-udev-detect tsched=0/' -i /etc/pulse/system.pa

## Services

COPY service/socat.service /etc/systemd/system/basic.target.wants/

# Run bluetooth and ofono services in debug mode
RUN sed 's@^ExecStart=/usr/lib/bluetooth/bluetoothd@ExecStart=/usr/lib/bluetooth/bluetoothd -d@' \
    -i /lib/systemd/system/bluetooth.service
RUN sed 's@^ExecStart=/usr/sbin/ofonod -n@ExecStart=/usr/sbin/ofonod -n -d@' \
    -i /lib/systemd/system/ofono.service

RUN adduser root pulse-access && \
    adduser pulse bluetooth && \
    adduser root bluetooth

RUN echo ForwardToConsole=yes >> /etc/systemd/journald.conf

ENV DISPLAY :0
ENV INITSYSTEM on
EXPOSE 7272:7272
CMD ["/usr/bin/pulseaudio", "--system", "--verbose", "--disallow-exit", "--disable-shm", "--exit-idle-time=-1"]
