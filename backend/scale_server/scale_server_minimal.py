#!/usr/bin/env python3

import socketio
import time

sio = socketio.Client()

@sio.event
def caller():
    sio.emit('data', "")

sio.connect('http://localhost:8080')

def main():
    while True:
        caller()
        time.sleep(0.01)

main()