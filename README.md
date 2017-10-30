## Building image

```sh
docker build -t bluez-sink .
```

## Building image on remote RPi

To connect to remote RPI run

```sh
PI_HOST=<pi_address>
PI_NAME=pi
ssh pi@$PI_HOST sudo sed 's/^ID=raspbian/ID=debian/' -i /etc/os-release
docker-machine create \
  --driver generic \
  --generic-ssh-user=pi \
  --generic-ip-address=$PI_HOST \
  --engine-storage-driver overlay2 \
  $PI_NAME
ssh pi@$PI_HOST sudo sed 's/^ID=debian/ID=raspbian/' -i /etc/os-release
eval $(docker-machine env $PI_NAME)
```

## Running image

```sh
docker run --tty -ti -v /var/run/dbus:/var/run/dbus -d /dev/ttyAMA0 --net=host bluez-sink bash
```

## Using external BT dongle

To use this with external BT dongle (required for HFP support via Ofono) you need to turn off bluetooth capabilities on host system:

```sh
mount -o remount rw /
systemctl stop bluetooth
systemctl disable bluetooth
systemctl mask bluetooth
```
