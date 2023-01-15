import RPi.GPIO as gpio
from controller import Controller


class GpioController(Controller):
    def __init__(self):
        self.pins = [21, 26, 20, 19, 16, 12, 22, 23, 27, 4]
        self.count = len(self.pins)
        gpio.setmode(gpio.BCM)
        for pin in self.pins:
            gpio.setup(pin, gpio.OUT)
            gpio.output(pin, gpio.LOW)

    def activate(self, index):
        gpio.output(self.pins[index], gpio.HIGH)

    def deactivate(self, index):
        gpio.output(self.pins[index], gpio.LOW)

    def cleanup(self):
        for pin in self.pins:
            gpio.output(pin, gpio.LOW)
