FROM resin/raspberrypi3-python

RUN apt-get update && apt-get install -yq --no-install-recommends python-dbus python-gobject

COPY *.py /agent/

ENV INITSYSTEM 0
ENV DBUS_SYSTEM_BUS_ADDRESS tcp:host=localhost,port=7272,family=ipv4
CMD ["python", "/agent/agent.py", "-c", "NoInputNoOutput"]
ENTRYPOINT []
