# TODO: Use https://docs.python.org/2/library/struct.html or
# http://bitstruct.readthedocs.io/en/latest/ instead of ctypes

class Message(Structure):
    _fields_ = [
        ("flags", c_uint8),
        ("length", c_uint8)]

class CanMessage(object):
    extended = False
    rtr = False
    arbitrationId = 0
    ecuId = 0
    length = 0
    data = []

    def __init__(self, raw_data):
        b''.
        const canExtByte = parcel.readUInt8(0)
        result.extended = readBit(7, canExtByte) === 1
        result.rtr = readBit(7, canExtByte) === 1

        result.length = parcel.readUInt8(1)

        const header = (parcel.readUInt16BE(2) << 16) | parcel.readUInt16BE(4)
        result.ecuId = readBits(0, 11, header)
        if (result.extended) {
            result.arbitrationId = readBits(12, 29, header)
        }

        for (let i=0
                i < result.length
                i + +) {
            result.data[i] = parcel.readUInt8(6 + i)
        }

        return result

def padLeft(str, expected_width, char=" "):
    result = str
    while len(result) < expected_width:
        result = char + result

    return result

export class CanMessage {


    public static fromRawParcel(parcel: Buffer): CanMessage {
        let result = new CanMessage()

        const canExtByte = parcel.readUInt8(0)
        result.extended = readBit(7, canExtByte) == = 1
        result.rtr = readBit(7, canExtByte) == = 1

        result.length = parcel.readUInt8(1)

        const header = (parcel.readUInt16BE(2) << 16) | parcel.readUInt16BE(4)
        result.ecuId = readBits(0, 11, header)
        if (result.extended) {
            result.arbitrationId = readBits(12, 29, header)
        }

        for (let i=0
             i < result.length
             i + +) {
            result.data[i] = parcel.readUInt8(6 + i)
        }

        return result
    }

    public dataAsHexString(): string {
        return this.data
        .map(byte= > byte.toString(16))
        .map(repr= > padLeft(repr, 2, "0"))
        .join(" ")
    }
}
