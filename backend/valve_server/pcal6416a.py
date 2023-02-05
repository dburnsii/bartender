from smbus2 import SMBus
from controller import Controller


class GpioController(Controller):
    def __init__(self, count=10):
        print("Initializing PCAL6416A Valve Controller")
        self.pins = [[0x02, 0x01], [0x02, 0x02], [0x02, 0x04], [0x02, 0x08], [0x02, 0x10], [0x02, 0x20], [0x02, 0x40], [0x02, 0x80], [0x03, 0x01], [0x03, 0x02], [0x03, 0x04], [0x03, 0x08], [0x03, 0x10], [0x03, 0x20], [0x03, 0x40], [0x03, 0x80]]
        self.count = count
        self.bus = SMBus(1)
        self.address = 0x20

        # Turn off all outputs
        self.bus.write_byte_data(self.address, 0x02, 0x00)
        self.bus.write_byte_data(self.address, 0x03, 0x00)

        # Set all pins to outputs
        self.bus.write_byte_data(self.address, 0x06, 0x00)
        self.bus.write_byte_data(self.address, 0x07, 0x00)

    def activate(self, index):
        if index >= self.count or index < 0:
            print("Invalid pin: {}".format(index))
            return
        pin = self.pins[index]
        status = self.bus.read_byte_data(self.address, pin[0])
        self.bus.write_byte_data(self.address, pin[0], status | pin[1])

    def deactivate(self, index):
        if index >= self.count or index < 0:
            print("Invalid pin: {}".format(index))
            return
        pin = self.pins[index]
        status = self.bus.read_byte_data(self.address, pin[0])
        self.bus.write_byte_data(self.address, pin[0], status & ~pin[1])

    def cleanup(self):
        self.bus.write_byte_data(self.address, 0x02, 0x00)
        self.bus.write_byte_data(self.address, 0x03, 0x00)


import time
g = GpioController()
g.activate(0)
time.sleep(0.3)
g.deactivate(0)
time.sleep(0.5)
g.cleanup()