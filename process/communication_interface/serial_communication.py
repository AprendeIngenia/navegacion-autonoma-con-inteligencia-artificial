import serial


class SerialCommunication:
    def __init__(self):
        self.com = serial.Serial("COM9", 115200, write_timeout=10)

    def sending_data(self, command: bytes) -> None:
        self.com.write(command)