FROM resin/raspberrypi3-debian:jessie

RUN echo deb http://ftp.debian.org/debian jessie-backports main >> /etc/apt/sources.list && \
    gpg --keyserver pgpkeys.mit.edu --recv-key 8B48AD6246925553 && \
    gpg --keyserver pgpkeys.mit.edu --recv-key 7638D0442B90D010 && \
    gpg -a --export 8B48AD6246925553 | sudo apt-key add -- && \
    gpg -a --export 7638D0442B90D010 | sudo apt-key add --

RUN apt-get update && \
    apt-get install -y bluez bluez-firmware socat ofono && \
    apt-get -t jessie-backports install -y pulseaudio pulseaudio-module-bluetooth

COPY conf/pulseaudio-bluetooth.conf /etc/dbus-1/system/

# Backup ofono configuration file
RUN cp /etc/dbus-1/system.d/ofono.conf /etc/dbus-1/system.d/ofono.conf.bak
COPY conf/ofono.conf /etc/dbus-1/system.d/

# TODO: Ideally DB should reconnect to last device automatically
RUN cp /etc/bluetooth/main.conf /etc/bluetooth/main.conf.old
COPY conf/bluetooth-main.conf /etc/bluetooth/main.conf

# RUN echo "load-module module-switch-on-connect" >> /etc/pulse/system.pa && \
#     echo "load-module module-bluetooth-discover headset=ofono" >> /etc/pulse/system.pa && \
RUN echo "load-module module-bluetooth-policy" >> /etc/pulse/system.pa && \
    echo "load-module module-bluetooth-discover headset=ofono" >> /etc/pulse/system.pa

## Services

COPY service/socat.service /etc/systemd/system/basic.target.wants/

# Run bluetooth and ofono services in debug mode
RUN sed 's@^ExecStart=/usr/lib/bluetooth/bluetoothd@ExecStart=/usr/lib/bluetooth/bluetoothd -d@' \
    -i /lib/systemd/system/bluetooth.service
# RUN sed 's@^ExecStart=/usr/sbin/ofonod -n@ExecStart=/usr/sbin/ofonod -n -d@' \
#     -i /lib/systemd/system/ofono.service

RUN usermod -aG bluetooth,pulse-access,audio root && \
    usermod -aG bluetooth pulse

RUN echo ForwardToConsole=yes >> /etc/systemd/journald.conf

ENV DISPLAY :0
ENV INITSYSTEM on
EXPOSE 7272:7272

RUN echo "enable-remixing = yes" >> /etc/pulse/daemon.conf

CMD ["/usr/bin/pulseaudio", "--system", "--verbose", "--disallow-exit", "--exit-idle-time=-1"]
