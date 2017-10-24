import bitstruct

class CanMessage(object):
    FLAGS_FORMAT = bitstruct.compile("p1b1b1p5u8p3u18u11")

    def __init__(self, raw_data):
        self.extended = False
        self.rtr = False
        self.arbitration_id = 0
        self.ecu_id = 0
        self.length = 0
        self.data = b''

        extended, rtr, length, arbitration_id, ecu_id = \
            CanMessage.FLAGS_FORMAT.unpack(raw_data)

        self.length = length
        self.extended, self.rtr = extended, rtr
        self.arbitration_id, self.ecu_id = arbitration_id, ecu_id
        if not self.extended:
            self.arbitration_id = 0

        self.data = raw_data[6:6 + self.length]
