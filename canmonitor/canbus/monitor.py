import asyncio
from serial_asyncio import create_serial_connection
from canbus.protocol import CanbusProtocol

DEFAULT_PORT = {
    "win32": "COM3",
    "darwin": "/dev/cu.SLAB_USBtoUART",
    "linux": "/dev/ttyUSB0"
}

class CanPrinter(object):
    """A simple can bus messages console printer"""
    @staticmethod
    def send(message):
        print(message)

printer = CanPrinter()
S = create_serial_connection(asyncio.get_event_loop(),
                             CanbusProtocol.factory(printer),
                             DEFAULT_PORT["darwin"], baudrate=9600)

asyncio.get_event_loop().run_until_complete(S)
asyncio.get_event_loop().run_forever()
