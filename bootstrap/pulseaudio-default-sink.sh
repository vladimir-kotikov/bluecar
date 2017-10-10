#!/bin/bash -e
USBDEV=`pactl list sinks short | grep -m1 usb | cut -f1`
if [ ! -z $USBDEV ]; then
    cat /etc/pulse/system.pa | grep -q "^set-default-sink.*$" && \
    sed -i "s/^set-default-sink.*$/set-default-sink $USBDEV/" /etc/pulse/system.pa || \
    echo set-default-sink $USBDEV >> /etc/pulse/system.pa
fi
