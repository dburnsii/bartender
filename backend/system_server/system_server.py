#!/usr/bin/python3

import time
import socketio
import sys
import rpi_backlight

simulation = True

sio = socketio.Client()
backlight = None


@sio.event
def screen_brightness(data):
    if not simulation:
        global backlight
        backlight.brightness = int(data["value"])
    else:
        print("Setting backlight to '{}'".format(data["value"]))


@sio.event
def idle(data):
    # TODO: Maybe turn the screen off eventually? backlight.power = False
    pass


@sio.event
def connect():
    print("Connected to socket server.")
    sio.emit("register", {"name": "system"})


@sio.event
def simulation(data):
    global simulation
    global backlight
    print("Updating simulation status.")
    simulation = data["status"]

    if simulation:
        print("Simulating brightness change")
    else:
        backlight = rpi_backlight.Backlight()


@sio.event
def disconnect():
    print("Disconnected from server.")
    sys.exit(0)


sio.connect("http://localhost:8080")

while 1:
    time.sleep(0.25)
    sio.emit("ping", "")
