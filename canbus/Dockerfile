FROM resin/raspberrypi3-debian

RUN apt-get update && apt-get install -yq --no-install-recommends \
        python3 python-dbus python-gobject libsystemd \
    pip install cython adbus pyserial-asyncio

COPY *.py /canmonitor/

ENV INITSYSTEM 0
ENV DBUS_SYSTEM_BUS_ADDRESS tcp:host=localhost,port=7272,family=ipv4
CMD ["python", "/canmonitor/monitor.py"]
