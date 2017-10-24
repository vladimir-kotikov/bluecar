from canbus.message import CanMessage

TEST_DATA = bytes([
    0x31, 0x08,     # FLAGS, LEN
    0x00, 0x00,     # IDH
    0x06, 0x25,     # IDL
    0x01, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
])

def test_format():
    assert CanMessage.FLAGS_FORMAT.calcsize() == 8 * 6

def test_message_parse():
    message = CanMessage(raw_data=TEST_DATA)

    assert message.length == 8
    assert message.arbitration_id == 0
    assert message.ecu_id == 0x625
    assert message.data == b'\x01\x08\x00\x00\x00\x00\x00\x00'


def test_empty_message():
    message = CanMessage(raw_data=b'\x31\x00\x00\x00\x06\x25')

    assert message.length == 0
    assert message.data == b''
