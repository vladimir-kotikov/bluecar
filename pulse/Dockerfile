FROM resin/raspberrypi3-debian:stretch

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    pulseaudio pulseaudio-module-bluetooth

RUN apt-get install -yq --no-install-recommends mpg123
COPY ./BlueZedEx.mp3 /

RUN echo "resample-method = ffmpeg" >> /etc/pulse/daemon.conf
RUN echo "load-module module-switch-on-connect" >> /etc/pulse/system.pa
RUN sed 's/^load-module module-console-kit/#load-module module-console-kit/' -i /etc/pulse/system.pa
RUN sed 's/^load-module module-bluez4-discover/#load-module module-bluez4-discover/' -i /etc/pulse/system.pa

COPY alsa-base.conf /etc/modprobe.d/

RUN systemctl disable dbus

ENV DISPLAY :0
ENV INITSYSTEM on
ENV DBUS_SYSTEM_BUS_ADDRESS tcp:host=localhost,port=7272,family=ipv4

CMD ["/usr/bin/pulseaudio", "--verbose", "--disallow-exit", "--disable-shm", "--system", "--exit-idle-time=-1"]
