#!/usr/bin/python3

import time
import json
import socketio
from pydbus import SystemBus

print("Starting WiFi Server.")

simulation = True
sio = socketio.Client()

system_bus = SystemBus()
wpa_supplicant = system_bus.get("fi.wpa_supplicant1")

@sio.event
def connect():
    print("Connected to socket server.")
    sio.emit("register", {"name": "wifi"})


@sio.event
def simulation(data):
    global simulation
    global apt_cache
    print("Updating simulation status.")
    simulation = data["status"]

@sio.event
def disconnect():
    print("Disconnected from server.")
    sys.exit(0)


sio.connect("http://localhost:8080")

lastping = datetime.now()

while 1:
    time.sleep(0.01)
    if(datetime.now() - lastping > timedelta(seconds=5)):
        lastping = datetime.now()
        sio.emit('ping', "")
