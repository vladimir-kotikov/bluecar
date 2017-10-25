import asyncio
import logging
import ravel

POLL_INTERVAL = 3
OBJ_MANAGER_IFACE = "org.freedesktop.DBus.ObjectManager"
MEDIA_CONTROL_IFACE = "org.bluez.MediaControl1"
MEDIA_PLAYER_IFACE = "org.bluez.MediaPlayer1"
BLUEZ_BUS_NAME = "org.bluez"
ROOT = "/"


class MediaSearcher(object):

    @staticmethod
    async def find_devices(bus):
        """Finds all devices connected to default
        adapter (hci0) providing media control capabilities
        """

        obj_manager = await bus[BLUEZ_BUS_NAME][ROOT].get_async_interface(OBJ_MANAGER_IFACE)
        objects = await obj_manager.GetManagedObjects()

        def is_connected(iface): return iface.get("Connected")[1] is True

        # GetManagedObjects seem to always return an array of 1 object
        # so probably it's enough to take just first element
        return [path for path, ifaces in objects[0].items()
                if MEDIA_CONTROL_IFACE in ifaces and
                is_connected(ifaces[MEDIA_CONTROL_IFACE])]

    @staticmethod
    async def device_available(bus):
        """Waits for at least one available device"""
        available = await MediaSearcher.find_devices(bus)
        while not available:
            await asyncio.sleep(3)
            available = await MediaSearcher.find_devices(bus)

        return available


if __name__ == '__main__':
    from aioconsole import ainput
    from dbus.mediaplayer import MediaPlayer

    BUS = ravel.system_bus()
    BUS.attach_asyncio()

    LOOP = asyncio.get_event_loop()
    media_devices = LOOP.run_until_complete(
        MediaSearcher.device_available(BUS))
    DEVICE = str(media_devices[0])

    proxy = MediaPlayer(BUS, device_path=DEVICE + "/player0")

    async def poll_for_command():
        while True:

            intf = await proxy._proxy
            name = await intf.Name
            position = await intf.Position
            print ("Name %s: %s" % (name, position))

            await asyncio.sleep(5)

            # C = await ainput("Enter command (n,p): ")

            # print ("Command: %s" % C)

            # if C.strip() == "n":
            #     await proxy.fast_forward()
            # elif C.strip() == "p":
            #     await proxy.rewind()
            # else:
            #     print("Unknown command...")

    LOOP.run_until_complete(poll_for_command())
    LOOP.close()
