#!/usr/bin/python3

import time
import json
import socketio
import atexit
import sys
import math
from datetime import datetime, timedelta
from enum import Enum
from led_utils import rgb_multiply, simulate_pixels, color_to_tuple, mix

# Disable this to avoid printing pixels to the terminal
display_simulation = True

simulation = True
cup_presence_status = False
pixels = None

sio = socketio.Client()

# Temporarily hard-code the location of each bottle
bottle_index = [500, 2000, 3500, 5500, 7500, 11000, 12000, 14000, 16000, 17750]


@atexit.register
def cleanup():
    pass


class Mode(Enum):
    IDLE = 1
    ACTIVE = 2
    HIGHLIGHT = 3
    PROGRESS = 4


class BartenderPixels(list):
    def __init__(self, simulation=True, count=72, led_max=255, fps=30):
        self.simulation = simulation
        self.count = count
        self.led_max = led_max
        self.fps = fps
        self.idle_index = 0
        self.idle_direction = 1
        self.current_mode = Mode.IDLE
        self.range = self.led_max * self.count
        self.last_show = datetime.now()
        self.mode = Mode.IDLE
        self.idle_color = (0, 0, self.led_max)
        if simulation:
            list.__init__(self, [(0, 0, 0) for i in range(self.count)])
        else:
            import board
            from neopixel import NeoPixel
            self.neopixel = NeoPixel(self,
                                     board.D18,
                                     self.count,
                                     auto_write=False)

    def show(self):
        if(datetime.now() - self.last_show > timedelta(seconds=(1/self.fps))):
            self.last_show = datetime.now()
            if self.simulation:
                simulate_pixels(self)
            else:
                self.neopixel[0:-1] = self[0:-1]
                self.neopixel.show()

    def clear(self):
        self[0:self.count] = [(0, 0, 0) for i in range(self.count)]
        self.show()

    def highlight(self, indices, colors=None, spread=10):
        if not isinstance(indices, list):
            indices = [indices]

        if colors is None:
            colors = [(255, 255, 255) for i in range(len(indices))]
        elif isinstance(colors[0], int):
            colors = list(map(lambda x: color_to_tuple(x), colors))

        # Set all pixels to black inititally
        self[0:self.count] = [(0, 0, 0) for i in range(self.count)]

        i = 0
        for index in indices:
            # Initialize variables for incrementing later
            spread_range_upper = (self.led_max * spread / 2)
            spread_range_lower = (self.led_max * spread / 2)
            lower = 0
            upper = 0

            # Either set the center LED, or set the two closest to the index
            if index % self.led_max:
                lower = math.floor(index / self.led_max)
                upper = math.ceil(index / self.led_max)
                spread_range_upper -= ((upper * self.led_max) - index)
                spread_range_lower -= (index - (lower * self.led_max))
            else:
                lower = math.floor(index / self.led_max - 1)
                upper = math.floor(index / self.led_max + 1)
                self[lower + 1] = \
                    mix(self[lower+1], rgb_multiply(colors[i], 1))
                spread_range_upper -= self.led_max
                spread_range_lower -= self.led_max

            # Spread the value until reaching the spread limit
            while spread_range_upper > 0 or spread_range_lower > 0:
                if lower >= 0:
                    intensity = \
                        min(spread_range_lower, self.led_max) / self.led_max
                    self[lower] = \
                        mix(self[lower], rgb_multiply(colors[i], intensity))
                    lower -= 1
                spread_range_lower -= self.led_max
                if upper < self.count:
                    intensity = \
                        min(spread_range_upper, self.led_max) / self.led_max
                    self[upper] = \
                        mix(self[upper], rgb_multiply(colors[i], intensity))
                    upper += 1
                spread_range_upper -= self.led_max
            self.show()
            i += 1

    def update(self, idle_increment=50):
        if(self.mode == Mode.IDLE and datetime.now() - self.last_show >
                timedelta(seconds=(1/self.fps))):
            self.idle_index += self.idle_direction * idle_increment
            if self.idle_index >= self.range:
                self.idle_index = self.range - self.led_max
                self.idle_direction *= -1
            elif self.idle_index < 0:
                self.idle_index = 0
                self.idle_direction *= -1
            self.highlight(self.idle_index)
        self.show()

    def set_mode(self, mode):
        self.mode = mode

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    def rainbow_cycle(self):
        '''
        Currently unused, but could be used for rainbow animations
        '''
        for j in range(255):
            for i in range(self.count):
                rc_index = (i * 256 // self.count) + j
                self[i] = self.wheel(rc_index & 255)
            self.show()
            time.sleep(0.01)


@sio.event
def manual_pour_status(data):
    if(data['complete']):
        idle(None)
    elif data["percentage"] >= 0 and data["percentage"] <= 100:
        # TODO: Enclosing animation
        pass


@sio.event
def activate_valve(data):
    global cup_presence_status
    global pixels
    pixels.set_mode(Mode.ACTIVE)
    pixels.highlight(bottle_index[data['pin']])


@sio.event
def highlight_bottles(data):
    global pixels
    pixels.set_mode(Mode.ACTIVE)
    if 'colors' in data:
        pixels.highlight(list(map(lambda x: bottle_index[x], data['pins'])),
                         colors=data['colors'],
                         spread=5)
    else:
        pixels.highlight(list(map(lambda x: bottle_index[x], data['pins'])),
                         spread=5)


@sio.event
def deactivate_valve(data):
    pass


@sio.event
def deactivate_valves(data=None):
    pass


@sio.event
def cup_presence(data):
    global cup_presence_status
    cup_presence_status = data["present"]


@sio.event
def idle(data):
    global pixels
    pixels.set_mode(Mode.IDLE)


@sio.event
def connect():
    print("Connected to socket server.")
    sio.emit("register", {"name": "led"})


@sio.event
def simulation(data):
    global simulation
    global pixels
    global pixel_count
    global display_simulation
    print("Updating simulation status.")
    simulation = data["status"]

    pixels = BartenderPixels(simulation=simulation)


@sio.event
def disconnect():
    print("Disconnected from server.")
    sys.exit(0)


sio.connect("http://localhost:8080")

lastping = datetime.now()
lastshow = datetime.now()

while 1:
    time.sleep(0.01)
    if(datetime.now() - lastping > timedelta(seconds=5)):
        lastping = datetime.now()
        sio.emit('ping', "")
    if(pixels):
        #pixels.rainbow_cycle()
        pixels.update()
