from dbus.proxy import DBusProxy, proxy_method, proxy_property

MEDIA_CONTROL_IFACE = "org.bluez.MediaControl1"

class MediaControl(DBusProxy):
    def __init__(self, bus, device=None, adapter="hci0", device_path=None):
        if device is None and device_path is None:
            raise Exception("One of device od device_path arguments must be specified")

        path = device_path if device_path is not None \
                           else "/org/bluez/%s/%s" % (adapter, device)

        super().__init__(bus, path, MEDIA_CONTROL_IFACE)

    @proxy_method("Play")
    async def play(self):
        pass

    @proxy_method("Pause")
    async def pause(self):
        pass

    @proxy_method("Stop")
    async def stop(self):
        pass

    @proxy_method("Next")
    async def next(self):
        pass

    @proxy_method("Previous")
    async def previous(self):
        pass

    @proxy_method("VolumeUp")
    async def volume_up(self):
        pass

    @proxy_method("VolumeDown")
    async def volume_down(self):
        pass

    @proxy_method("FastForward")
    async def fast_forward(self):
        pass

    @proxy_method("Rewind")
    async def rewind(self):
        pass

    @property
    @proxy_property("Connected")
    def connected(self):
        pass
