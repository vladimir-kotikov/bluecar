import os
from unittest.mock import Mock

import asyncio
import pytest
import serial_asyncio

from canbus.protocol import CanbusProtocol
from canbus.message import CanMessage

HOST = '127.0.0.1'
_PORT = 8888

# on which port should the tests be performed:
PORT = 'socket://%s:%s' % (HOST, _PORT)
TEXT = b'Hello, World!\n'

class FakeProtocol(asyncio.Protocol):
    def __init__(self):
        super().__init__()
        self._transport = None

    def connection_made(self, transport):
        self._transport = transport
        self._transport.write(TEXT)
        self._transport.write_eof()

    def connection_lost(self, exc):
        self._transport._loop.stop()

@pytest.mark.skipif(os.name != 'posix', reason="asyncio not supported on platform")
def test_asyncio():
    loop = asyncio.get_event_loop()

    coro = loop.create_server(FakeProtocol, HOST, _PORT)
    loop.run_until_complete(coro)

    sender_mock = Mock(spec=["send"])
    client = serial_asyncio.create_serial_connection(
        loop, CanbusProtocol.factory(sender_mock), PORT)
    loop.run_until_complete(client)

    loop.run_forever()
    loop.close()

    sender_mock.send.assert_called_once()
    mock_args = sender_mock.send.call_args[0]
    assert isinstance(mock_args[0], CanMessage)
