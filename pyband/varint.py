def varint_encode(value):
    rawdata = []
    while True:
        towrite = value & 0x7F
        value >>= 7
        if value != 0:
            rawdata.append(towrite | 0x80)
        else:
            rawdata.append(towrite)
            break
    return bytes(rawdata)


def varint_decode(data):
    value = 0
    for idx, toread in enumerate(list(data)):
        value |= (toread & 0x7F) << (7 * idx)
        if not (toread & 0x80):
            return value, data[idx+1:]
    raise ValueError("Unable to parse {} to unsigned integer".format(data))
