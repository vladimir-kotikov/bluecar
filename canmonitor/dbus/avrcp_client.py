import asyncio
import logging
import ravel

log_formatter = logging.Formatter(
    "%(asctime)s %(levelname).1s: [canmonitor] %(name)s: %(message)s")
log_handler = logging.StreamHandler()
log_handler.formatter = log_formatter

LOG = logging.getLogger("avrcp_client")
LOG.setLevel(logging.DEBUG)
LOG.addHandler(log_handler)

OBJ_MANAGER_IFACE = "org.freedesktop.DBus.ObjectManager"
MEDIA_CONTROL_IFACE = "org.bluez.MediaControl1"
BLUEZ_BUS_NAME = "org.bluez"
ROOT = "/"

POLL_INTERVAL = 5

@ravel.interface(ravel.INTERFACE.CLIENT, name="org.bluez.MediaControl1")
class MediaControlProxy(object):
    """
    Introspect XML for org.bluez.MediaControl1 interface
    <interface name="org.bluez.MediaControl1">
        <method name="Play"></method>
        <method name="Pause"></method>
        <method name="Stop"></method>
        <method name="Next"></method>
        <method name="Previous"></method>
        <method name="VolumeUp"></method>
        <method name="VolumeDown"></method>
        <method name="FastForward"></method>
        <method name="Rewind"></method>
        <property name="Connected" type="b" access="read"></property>
    </interface>
    """

    def __init__(self, bus):
        self._bus = bus

    async def find_media_devices(self):
        obj_manager = await self._bus[BLUEZ_BUS_NAME][ROOT]\
            .get_async_interface(OBJ_MANAGER_IFACE)

        objects = await obj_manager.GetManagedObjects()

        # GetManagedObjects seem to always return an array of 1 object
        # so probably it's enough to take just first element
        objects_found = []
        for path, ifaces in objects[0].items():
            media_control_iface = ifaces.get(MEDIA_CONTROL_IFACE)
            if media_control_iface is None:
                continue

            LOG.debug("Found implementation of %s in %s", MEDIA_CONTROL_IFACE, path)
            _, connected = media_control_iface.get("Connected")
            LOG.debug("Connected: %s (type: %s)", connected, type(_))

            if connected is True:
                objects_found.append(path)

        return objects_found

    async def poll_for_devices(self):

        LOG.info("Searching for available media devices...")
        avail_devices = await self.find_media_devices()
        while not avail_devices:
            LOG.info("Didn't find any media control devices, " +
                     "attempting once more in %s seconds...", POLL_INTERVAL)

            await asyncio.sleep(3)
            avail_devices = await self.find_media_devices()

        LOG.info("Found %d media control device%s", len(avail_devices),
                 len(avail_devices) > 1 and "s" or "")

        return avail_devices


if __name__ == '__main__':
    LOOP = asyncio.get_event_loop()

    BUS = ravel.system_bus()
    BUS.attach_asyncio(LOOP)

    asyncio.Task()

    media_devices = LOOP.run_until_complete(MediaControlProxy(BUS).poll_for_devices())

    print(media_devices)
    LOOP.close()
