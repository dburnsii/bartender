#!/usr/bin/python3

import time
import json
import socketio
import atexit
import sys
import math
from datetime import datetime, timedelta
from enum import Enum

class Mode(Enum):
    IDLE = 1
    HIGHLIGHT = 2

# Disable this to avoid printing pixels to the terminal
display_simulation = True

led_max = 255
simulation = True
cup_presence_status = False
pixels = None
current_mode = Mode.IDLE
idle_index = 0
idle_direction = 1

pixel_count = 60
pixel_range = led_max * pixel_count
pixel_fps = 30

RED = (led_max, 0, 0)
GREEN = (0, led_max, 0)
BLUE = (0, 0, led_max)
WHITE = (led_max, led_max, led_max)

idle_color = WHITE

sio = socketio.Client()


@atexit.register
def cleanup():
    pass

def simulate_pixels():
    global pixels
    print("\r", end="")
    for pixel in pixels:
        print("\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(
                                                                    int(pixel[0]),
                                                                    int(pixel[1]),
                                                                    int(pixel[2]),
                                                                    "O"),
                                                                end='',
                                                                sep='',
                                                                flush=True)

def rgb_multiply(color, intensity=1):
    return tuple(map(lambda x: x * max(intensity, 0), color))

def show_pixels():
    global pixels
    global simulation
    global display_simulation
    if simulation and display_simulation:
        simulate_pixels()
    else:
        pixels.show()

def highlight(index, spread=10):
    global led_max
    global pixels
    global pixel_count

    pixels[0:pixel_count] = [(0,0,0) for i in range(pixel_count)]

    spread_range_upper = (led_max * spread / 2)
    spread_range_lower = (led_max * spread / 2)
    lower = 0
    upper = 0
    if index % led_max:
        lower = math.floor(index / led_max)
        upper = math.ceil(index / led_max)
        spread_range_upper -= ( ( upper * led_max) - index)
        spread_range_lower -= ( index - ( lower * led_max))
    else:
        lower = math.floor(index / led_max - 1)
        upper = math.floor(index / led_max + 1)
        pixels[lower + 1] = rgb_multiply(idle_color, 1)
        spread_range_upper -= led_max
        spread_range_lower -= led_max
    while spread_range_upper > 0 or spread_range_lower > 0:
        if lower >= 0:
            intensity = min(spread_range_lower, led_max) / led_max
            pixels[lower] = rgb_multiply(idle_color, intensity)
            lower -= 1
        spread_range_lower -= led_max
        if upper < pixel_count:
            intensity = min(spread_range_upper, led_max) / led_max
            pixels[upper] = rgb_multiply(idle_color, intensity)
            upper += 1
        spread_range_upper -= led_max

def update_idle(increment=50):
    global simulation
    global pixels
    global pixel_count
    global idle_index
    global idle_direction
    idle_index += idle_direction * increment
    if idle_index >= pixel_range:
        idle_index = pixel_range - led_max
        idle_direction *= -1
    elif idle_index < 0:
        idle_index = 0
        idle_direction *= -1
    highlight(idle_index)



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
    if not simulation:
        if cup_presence_status:
            print("Activating leds above valve {}".format(data['pin']))
            # TODO: Highlight bottle
    else:
        print("Simulating LED activation on valve {}".format(data['pin']))


@sio.event
def highlight_bottles(data):
    print("Highlighting leds above valve {}".format(data['pins']))
    # TODO highlight bottle


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
    global current_mode
    current_mode = Mode.IDLE


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

    if simulation:
        pixels = [(0,0,0) for i in range(pixel_count)]
        if display_simulation:
            print("o", end="")
    else:
        import board
        import neopixel
        pixels = neopixel.NeoPixel(board.D18, pixel_count, auto_write=False)


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
    if(datetime.now() - lastshow > timedelta(seconds=(1/pixel_fps))):
        lastshow = datetime.now()
        if current_mode == Mode.IDLE:
            update_idle()
        show_pixels()
