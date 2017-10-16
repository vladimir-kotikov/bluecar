```sh
#!/bin/sh

echo $USER

USERNAME="pi"
[[ -z "$1" ]] && USERNAME="$1"

# Update and install dependencies
apt-get update
apt-get -y upgrade
apt-get -y --no-install-recommends install \
    bluez bluez-tools pulseaudio pulseaudio-module-bluetooth pulseaudio-utils

## Authorize users (each user that will be using PA must belong to group pulse-access)
adduser "$USERNAME" pulse-access

# Authorize PulseAudio - which will run as user pulse - to use BlueZ D-BUS interface:
cat <<EOF >/etc/dbus-1/system.d/pulseaudio-bluetooth.conf
<busconfig>
  <policy user="pulse">
    <allow send_destination="org.bluez"/>
  </policy>
</busconfig>
EOF

# Make USB sound preferred over analog
cat <<EOF >/etc/modprobe.d/alsa-base.conf
# This sets the index value of the cards but doesn't reorder.
options snd_usb_audio index=0
options snd_bcm2835 index=1

# Does the reordering.
options snd slots=snd_usb_audio,snd_bcm2835
EOF

# Configure pulseaudio - change "resample-method"
echo "resample-method = ffmpeg" > /etc/pulse/daemon.conf
# Available on PA11 only. See https://www.freedesktop.org/wiki/Software/PulseAudio/Notes/11.0/
# echo "avoid-resampling = yes" > /etc/pulse/daemon.conf

# PulseAudio (both version 2 and 5) has a problem with the Pi's on-board sound driver.
# If you are not using a USB sound card, the following work-around helps to remove stuttering and other problems
# https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=87138#p619713


# Load  Bluetooth discover and policy modules in SYSTEM MODE
# See https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/#index36h3
cat <<EOF >> /etc/pulse/system.pa

### Automatically load driver modules for Bluetooth hardware
.ifexists module-bluetooth-discover.so
load-module module-bluetooth-discover
.endif

.ifexists module-bluetooth-policy.so
load-module module-bluetooth-policy
.endif
EOF

# Create and start a systemd service for running pulseaudio in System Mode as user "pulse".
cat <<EOF >/etc/systemd/system/pulseaudio.service
[Unit]
Description=Pulse Audio

[Service]
Type=simple
ExecStart=/usr/bin/pulseaudio --system --disallow-exit --disable-shm --exit-idle-time=-1

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable pulseaudio.service

# Set usb audio card as default
# TODO: probably need to be set as udev rule trigger
USBDEV=`pactl list sinks short | grep -m1 usb | cut -f1`
if [ ! -z $USBDEV ]; then
  cat /etc/pulse/system.pa | grep -q "^set-default-sink.*$" && \
    sed -i "s/^set-default-sink.*$/set-default-sink $USBDEV/" /etc/pulse/system.pa || \
    echo set-default-sink $USBDEV >> /etc/pulse/system.pa
fi

pulseaudio -k
systemctl start pulseaudio.service
```
