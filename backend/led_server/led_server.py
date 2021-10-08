#!/usr/bin/python3

import serial
import time
import json
import serial.tools.list_ports
import socketio
import atexit
import sys
from datetime import datetime, timedelta

serial_queue = []

simulation = True
cup_presence_status = False
serial_ready = False

sio = socketio.Client()


@atexit.register
def cleanup():
    if not simulation:
        tty.close()


def serial_write(data):
    if isinstance(data, dict):
        data = json.dumps(data)
    if not simulation and serial_ready:
        tty.write((data + "\x00").encode())
    else:
        print("Writing: {}".format(data))


@sio.event
def manual_pour_status(data):
    global serial_queue
    if(data['complete']):
        idle(None)
    elif data["percentage"] >= 0 and data["percentage"] <= 100:
        serial_queue.append({"command": "drinkProgress", "progress": data["percentage"] * 100})

@sio.event
def activate_valve(data):
    global serial_queue
    global cup_presence_status
    if not simulation:
        if cup_presence_status:
            print("Activating leds above valve {}".format(data['pin']))
            if("colors" in data):
                serial_queue.append({"command": "highlight",
                              "locations": [data['pin']],
                              "colors": data['colors']})
            else:
                serial_queue.append({"command": "highlight",
                              "locations": [data['pin']]})
    else:
        print("Simulating LED activation on valve {}".format(data['pin']))


@sio.event
def highlight_bottles(data):
    global serial_queue
    print("Highlighting leds above valve {}".format(data['pins']))
    if("colors" in data):
        serial_queue.append({"command": "highlight",
                      "locations": data['pins'],
                      "colors": data['colors']})
    else:
        serial_queue.append({"command": "highlight",
                      "locations": data['pins']})


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
    global serial_queue
    serial_queue.append({"command": "idle"})


@sio.event
def connect():
    print("Connected to socket server.")
    sio.emit("register", {"name": "led"})


@sio.event
def simulation(data):
    global simulation
    global serial_ready
    print("Updating simulation status.")
    simulation = data["status"]

    if not simulation:
        global tty
        ports = serial.tools.list_ports.comports()
        arduino_port = ""
        for port in ports:
            if "Arduino" in port[1]:
                print("Found arduino on port {}".format(port[0]))
                arduino_port = port[0]
                break
        if not arduino_port:
            print("No Arduino found")
            return
        tty = serial.Serial(arduino_port, 115200, timeout=2)
        # Allow Arduino to reset due to new connection
        time.sleep(2)
        serial_ready = True
        print("Serial port ready!")


@sio.event
def disconnect():
    print("Disconnected from server.")
    sys.exit(0)


sio.connect("http://localhost:8080")

lastping = datetime.now()

while 1:
    time.sleep(0.01)
    if(serial_queue):
        serial_write(serial_queue[-1])
        serial_queue = []
    if(datetime.now() - lastping > timedelta(seconds=5)):
        lastping = datetime.now()
        sio.emit('ping', "")
