import board
import busio
from digitalio import Direction
from adafruit_mcp230xx.mcp23008 import MCP23017

from controller import Controller


class GpioController(Controller):
    def __init__(self, count=10):
        self.pins = [8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7]
        self.count = count
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mcp = MCP23017(i2c)

        for i in range(self.count):
            pin = mcp.get_pin(self.pins[i])
            pin.direction = Direction.OUTPUT
            pin.value = False

    def activate(self, index):
        if index >= count or index < 0:
            print("Invalid pin: {}".format(index))
            return
        pin = self.mcp.get_pin(self.pins[index])
        pin.value = True

    def deactivate(self, index):
        if index >= count or index < 0:
            print("Invalid pin: {}".format(index))
            return
        pin = self.mcp.get_pin(self.pins[index])
        pin.value = True

    def cleanup(self):
        for pin_index in self.pins:
            pin = self.mcp.get_pin(pin_index)
            pin.value = False
