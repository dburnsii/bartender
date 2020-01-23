#!/usr/bin/python

import json
import importlib
import time
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
gpio_lib = importlib.util.find_spec('RPi')
board_lib = importlib.util.find_spec('board')
busio_lib = importlib.util.find_spec('busio')
mcp_lib = importlib.util.find_spec('adafruit_mcp230xx')

if gpio_lib and board_lib and busio_lib and mcp_lib:
    testing = False
    import RPi.GPIO as GPIO
    import board
    import busio
    from adafruit_mcp230xx.mcp23017 import MCP23017
    i2c = busio.I2C(board.SCL, board.SDA)
else:
    testing = True

PORT = 8080
led_upper_pins = [12, 13, 14]
led_lower_pins = [15, 16, 17]
led_upper_value = 16777215
led_lower_value = 1052688
current_drink = []
mcp = None  # MCP23017 GPIO Device for controlling the motors
mcp_address = 0x20


def millis():
    return int(round(time.time() * 1000))


def init_motors():
    print("Initializing pump interface")
    global mcp
    global i2c
    mcp = MCP23017(i2c, address=mcp_address)
    mcp.iodir = 0
    mcp.gpio = 0xFFFF


def get_led_upper():
    return led_upper_value


def set_led_upper(value):
    global led_upper_value
    led_upper_value = value
    return "Success!"


def get_led_lower():
    return led_lower_value


def set_led_lower(value):
    global led_lower_value
    led_lower_value = value
    return "Success!"


def pour_drink(drink):
    """
    Handles the activation of motors and setting of drink array to stop specified motors when pour time has elapsed.
    :param drink : dict, Contains I2C Addresses (as Ints) and Pour times (in milliseconds) needed to pour specified drink.

    :return: int , ETA of drink being poured.
    """

    if testing:
        print("Pouring a drink!!")
    else:
        mcp.get_pin(3).value = False
        time.sleep(3)
        mcp.get_pin(3).value = True
        return millis() + 5000


def run_server():
    server_address = ("localhost", PORT)
    httpd = HTTPServer(server_address, WorkerServer)
    print("Serving at " + str(server_address))
    httpd.serve_forever()


class WorkerServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        return "test!".encode("utf8")

    def do_GET(self):
        response = ""
        query_string = urlparse(self.path).query
        query = parse_qs(query_string)
        print(query)
        if "get" in query:
            target = query["get"][0]
            if target == "led_upper":
                response = str(get_led_upper())
            elif target == "led_lower":
                response = str(get_led_lower())
            else:
                response = "Invalid query!"
        elif "set" in query:
            target = query["set"][0]
            if target == "led_upper":
                response = set_led_upper(int(query["value"][0]))
            elif target == "led_lower":
                response = set_led_lower(int(query["value"][0]))
            else:
                response = "Invalid query!"
        elif "drink" in query:
            response = pour_drink("test")
        else:
            response = "Invalid Query!"

        self._set_headers()
        self.wfile.write(response.encode("utf8"))


def main():
    if testing:
        run_server()
    else:
        init_motors()
        run_server()


main()
