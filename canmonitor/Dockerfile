FROM resin/raspberrypi3-python:3.6

RUN pip install bitstruct==3.5.0 pyserial-asyncio==0.4 git+https://github.com/ldo/dbussy.git#egg=dbussy

ENV DISPLAY :0
ENV INITSYSTEM 0
ENV DBUS_SYSTEM_BUS_ADDRESS tcp:host=localhost,port=7272,family=ipv4
ENTRYPOINT [ ]

COPY . /canmonitor
CMD ["python", "/canmonitor/dbus/avrcp_client.py"]
