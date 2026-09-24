from embedded_framework.communication.modbusengine import ModbusRtuEngine


class _Serial:
    is_open = False

    def __init__(self):
        body = b"\x01\x03\x04\x00\x0a\x01\x02"
        self.response = body + ModbusRtuEngine._crc(body)
        self.sent = b""

    def open(self):
        self.is_open = True

    def reset_input_buffer(self):
        pass

    def write(self, data):
        self.sent = data

    def read(self, size):
        result, self.response = self.response[:size], self.response[size:]
        return result

    def close(self):
        self.is_open = False


def test_read_holding_registers():
    session = _Serial()
    assert ModbusRtuEngine(session).read_holding_registers(1, 0, 2) == [10, 258]
    assert session.sent == b"\x01\x03\x00\x00\x00\x02\xc4\x0b"
