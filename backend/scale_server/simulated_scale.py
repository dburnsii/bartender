#!/usr/bin/env python3

import time


class Simulator:
    def __init__(self):
        self.zero = 0
        self.readout = 0
        self.gain = 1
        print("Init simulated scale")

    def setup(self):
        print("Set up scale")

    def get_weight(self, count=3):
        for i in range(count):
            time.sleep(0.1)
        return self.readout - self.zero

    def reset(self):
        print("Reset")

    def set_gain(self, gain):
        self.gain = gain
        print("Set gain: {}".format(self.gain))

    def calibrate_offset(self):
        print("Calibrate")

    def tare(self):
        self.zero = self.get_weight(10)

    def cleanup(self):
        print("Cleaning up")


if __name__ == "__main__":
    adc = Simulator()
    adc.tare()

    while True:
        v = adc.get_weight()
        #print(v)
        time.sleep(0.2)
