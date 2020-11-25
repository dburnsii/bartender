#!/usr/bin/python3

import serial, time, json
import serial.tools.list_ports
import socketio
import atexit
import sys


simulation = True
cup_presence_status = False

def cleanup():
    if not simulation:
        tty.close()

sio = socketio.Client()

@sio.event
def activate_valve(data):
    global cup_presence_status
    if not simulation:
        if cup_presence_status:
            print("Activating leds above valve {}".format(data['pin']))
            if("colors" in data):
                tty.write((json.dumps({"command": "highlight", "locations": [data['pin']], "colors": data['colors']}) + "\x00").encode())
            else:
                tty.write((json.dumps({"command": "highlight", "locations": [data['pin']]}) + "\x00").encode())
    else:
        print("Simulating LED activation on valve {}".format(data['pin']))

@sio.event
def highlight_bottles(data):
    print("Activating leds above valve {}".format(data['pin']))
    if("colors" in data):
        tty.write((json.dumps({"command": "highlight", "locations": [data['pins']], "colors": data['colors']}) + "\x00").encode())
    else:
        tty.write((json.dumps({"command": "highlight", "locations": [data['pins']]}) + "\x00").encode())

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
    tty.write((json.dumps({"command": "idle"}) + "\x00").encode())

@sio.event
def connect():
    print("Connected to socket server.")
    sio.emit("register", {"name": "led"})

@sio.event
def simulation(data):
    global simulation
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
        tty = serial.Serial(arduino_port, 19200, timeout=2)
        # Allow Arduino to reset due to new connection
        time.sleep(2)
        print("Serial port ready!")


@sio.event
def disconnect():
    print("Disconnected from server.")
    sys.exit(0)

sio.connect("http://localhost:8080")

while 1:
    time.sleep(0.25)
    sio.emit("ping", "")
