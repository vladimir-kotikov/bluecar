from asyncio import Protocol
from logging import getLogger
from .message import CanMessage

LOG = getLogger(__name__)

class CanbusProtocol(Protocol):
    """Protocol for reading data from can bus over serial adapter"""
    def __init__(self, dbusMessageSender):
        self._sender = dbusMessageSender

    def data_received(self, data):
        LOG.debug("Received %s", repr(data))

        message = CanMessage(raw_data=data)
        self._sender.send(message)

    def eof_received(self):
        """Called when the other end calls write_eof() or equivalent"""
        LOG.info('Can adapter disconnected')
        # false value(including None) means that the transport
        # will close itself, otherwise closing the
        # transport is up to the protocol.
        return False

    @staticmethod
    def factory(dbus_sender):
        """Factory method to create protocol instance attached to dbus"""
        return lambda: CanbusProtocol(dbus_sender)