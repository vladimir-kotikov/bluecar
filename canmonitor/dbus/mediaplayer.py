from dbus.proxy import proxy_property
from dbus.mediacontrol import MediaControl

MEDIA_CONTROL_IFACE = "org.bluez.MediaPlayer1"

class MediaPlayer(MediaControl):
    def __init__(self, bus, device=None, device_path=None,
                 adapter="hci0", player_node="player0"):

        if device is None and device_path is None:
            raise Exception("One of device od device_path arguments must be specified")

        path = device_path if device_path is not None \
                           else "/org/bluez/%s/%s/%s" % (adapter, device, player_node)

        super().__init__(bus, device_path=path)

        self._interface = "org.bluez.MediaPlayer1"

    @property
    @proxy_property("Name")
    async def name(self):
        pass

    @property
    @proxy_property("Type")
    async def type(self):
        pass

    @property
    @proxy_property("Subtype")
    async def subtype(self):
        pass

    @property
    @proxy_property("Position")
    async def position(self):
        pass

    @property
    @proxy_property("Status")
    async def status(self):
        pass

    @property
    @proxy_property("Equalizer")
    async def equalizer(self):
        pass

    @property
    @proxy_property("Repeat")
    async def repeat(self):
        pass

    @property
    @proxy_property("Shuffle")
    async def shuffle(self):
        pass

    @property
    @proxy_property("Scan")
    async def scan(self):
        pass

    @property
    @proxy_property("Track")
    async def track(self):
        pass

    @property
    @proxy_property("Device")
    async def device(self):
        pass

    @property
    @proxy_property("Browsable")
    async def browsable(self):
        pass

    @property
    @proxy_property("Searchable")
    async def searchable(self):
        pass

    @property
    @proxy_property("Playlist")
    async def playlist(self):
        pass
