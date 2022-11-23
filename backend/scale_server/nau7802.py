#!/usr/bin/env python3

from smbus2 import SMBus
import time
import atexit

# Device Address
DA = 0x2A

# PU_CTRL Register
PU_CTRL = 0x00
RR = 0x01  # Register reset
PUD = 0x02  # Power-up digital circuit
PUA = 0x04  # Power-up analog circuit
PUR = 0x08  # Power-up Ready
CS = 0x10  # Cycle Start
CR = 0x20  # ADC Data is ready
OSCS = 0x40  # System clock select
AVDDS = 0x80  # AVDD Source Select

# CTRL1 Register
CTRL1 = 0x01
CRP = 0x80  # Converstion ready pin polarity
DRDY_SEL = 0x40  # DRDY pin function
VLDO = 0x34  # LDO Voltage (3 bits)
GAINS = 0x07  # Gain select (3 bits)

# CTRL2 Register
CTRL2 = 0x02
CHS = 0x80  # Channel select
CRS = 0x70  # Conversion rate select
CAL_ERR = 0x08  # Calibration error result
CALS = 0x04  # Calibration Trigger
CALMOD = 0x03  # Calibration mode select

# I2C_CTRL Register
I2C_CTRL = 0x11
CRSD = 0x80  # Enable SDA Low when ready
FRD = 0x40  # Enable fast read ADC data
SPE = 0x20  # Strong pullup for SCLK and SDA (1.6k Ohm)
WPD = 0x10  # Weak pullup for SCLK and SDA (50k Ohm) (default)
SI = 0x08  # Short the input together, measure offset
BOPGA = 0x04  # Enable 2.5uA burnout current source to GPA positive input
TS = 0x02  # Use Temperature Sensor
BGPCP = 0x01  # Disables bandgap chopper

ADC_B2 = 0x12
ADC_B1 = 0x13
ADC_B0 = 0x14


class NAU7802:
    def __init__(self, gain=128):
        self.bus = SMBus(0)
        self.gain = gain
        self.powered = False
        self.zero = 0
        self.reset()
        self.setup()

    def setup(self):
        if not self.powered:
            print("Reset chip first")

        # Enable cycle and internal LDO
        b = self.bus.read_byte_data(DA, PU_CTRL)
        self.bus.write_byte_data(DA, PU_CTRL, b | CS | AVDDS)

    def get_weight(self, count=3):
        output = 0
        for i in range(count):
            b = self.bus.read_byte_data(DA, PU_CTRL)
            start = time.time()
            while not (b & CR):
                b = self.bus.read_byte_data(DA, PU_CTRL)
            v = self.bus.read_i2c_block_data(DA, ADC_B2, 3)
            output += (v[0] << 16) + (v[1] << 8) + v[2]
        output = (output / count) - self.zero
        print(output)
        return output

    def reset(self):
        b = self.bus.read_byte_data(DA, PU_CTRL)
        self.bus.write_byte_data(DA, PU_CTRL, b | RR)
        self.powered = False
        time.sleep(1)
        b = self.bus.read_byte_data(DA, PU_CTRL)
        self.bus.write_byte_data(DA, PU_CTRL, PUD | PUA)
        while True:
            b = self.bus.read_byte_data(DA, PU_CTRL)
            if b & PUR:
                print("Powerup complete")
                self.powered = True
                break

    def set_gain(self, gain):
        gain = 0x00
        if self.gain == 128:
            gain = 0x07
        elif self.gain == 64:
            gain = 0x06
        elif self.gain == 32:
            gain = 0x05
        elif self.gain == 16:
            gain = 0x04
        elif self.gain == 8:
            gain = 0x03
        elif self.gain == 4:
            gain = 0x02
        elif self.gain == 2:
            gain = 0x01
        elif self.gain == 1:
            gain = 0x00
        else:
            print("Invalid gain")
            return
        b = self.bus.read_byte_data(DA, CTRL1)
        self.bus.write_byte_data(DA, CTRL1, (b | ~GAINS) | gain)
        self.gain = gain

    def calibrate_offset(self):
        b = self.bus.read_byte_data(DA, CTRL2)
        self.bus.write_byte_data(DA, CTRL2, (b | CALS))

        while True:
            b = self.bus.read_byte_data(DA, CTRL2)
            if not b & CALS:
                break
        print("Calibration offset: {}".format(
            self.bus.read_i2c_block_data(DA, 0x03, 3)))
        print("Calibration gain: {}".format(
            self.bus.read_i2c_block_data(DA, 0x06, 3)))
        b = self.bus.read_byte_data(DA, CTRL2) | CAL_ERR
        if b:
            print("calibration error")

    def tare(self):
        self.zero = self.get_weight(10)

    def cleanup(self):
        print("Cleaning up")
        self.bus.close()

# atexit.register(cleanup)

# if main:
#     adc = NAU7805()

#     adc.reset()
#     adc.setup()

#     time.sleep(1)

#     adc.calibrate_offset()

#     while True:
#         v = int((read() + read() + read())/ 3)
#         print(int(v/1000))
#         time.sleep(0.2)
