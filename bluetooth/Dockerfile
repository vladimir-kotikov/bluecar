FROM resin/raspberrypi3-debian:jessie

RUN echo deb http://ftp.debian.org/debian jessie-backports main >> /etc/apt/sources.list && \
    apt-key adv --keyserver pgp.mit.edu --recv-key 0x7638D0442B90D010 && \
    apt-get update && \
    apt-get install -y bluez bluez-firmware socat ofono && \
    apt-get -t jessie-backports install -y pulseaudio pulseaudio-module-bluetooth

COPY conf/ofono.conf /etc/dbus-1/system.d/
COPY conf/bluetooth.conf /etc/bluetooth/main.conf
COPY service/socat.service /etc/systemd/system/basic.target.wants/

RUN echo ForwardToConsole=yes >> /etc/systemd/journald.conf

RUN echo "resample-method = speex-fixed-8" >> /etc/pulse/daemon.conf && \
    echo "load-module module-bluetooth-policy" >> /etc/pulse/system.pa && \
    echo "load-module module-bluetooth-discover headset=ofono" >> /etc/pulse/system.pa

RUN usermod -aG bluetooth,pulse-access,audio root && \
    usermod -aG bluetooth pulse

ENV DISPLAY :0
ENV INITSYSTEM on
EXPOSE 7272:7272

CMD ["/usr/bin/pulseaudio", "--system", "--disallow-exit", "--exit-idle-time=-1"]
