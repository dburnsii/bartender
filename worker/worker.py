#!/usr/bin/python

import asyncio
import websockets
import json
import importlib


smbus_lib = importlib.util.find_spec('smbus')
gpio_lib = importlib.util.find_spec('RPi')

if smbus_lib is None or gpio_lib is None:
    testing = True
else:
   testing = False
   import smbus
   import RPi.GPIO as GPIO


async def socket(websocket, path):
    while True:
        name = await websocket.recv()
        data = json.loads(name)
        response = ""

        if "drink" in data:
            response = "Pouring drink!"
        elif "led_upper" in data:
            response = "Setting upper LED"
        elif "led_lower" in data:
            response = "Setting lower LED"
        elif "lcd" in data:
            response = "Setting LCD text"
        else:
            response = "Command not recognized: " + str(data)

        await websocket.send(response)

start_server = websockets.serve(socket, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
print("Listening on ws://localhost:8765")
asyncio.get_event_loop().run_forever()
