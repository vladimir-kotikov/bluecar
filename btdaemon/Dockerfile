FROM resin/raspberrypi3-debian:stretch

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    bluez bluez-firmware socat

COPY conf/bluetooth-main.conf /etc/bluetooth/main.conf
COPY conf/pulseaudio-bluetooth.conf /etc/dbus-1/system/

ENV INITSYSTEM on
EXPOSE 7272:7272
CMD (/usr/bin/hciattach /dev/ttyAMA0 bcm43xx 921600 noflow - || \
     /usr/bin/hciattach /dev/ttyAMA0 bcm43xx 921600 noflow -) && \
    systemctl start bluetooth && \
    /usr/bin/socat TCP-LISTEN:7272,reuseaddr,fork UNIX-CONNECT:/var/run/dbus/system_bus_socket
