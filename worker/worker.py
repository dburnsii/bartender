#!/usr/bin/python

import json
import importlib
import os
import threading
import time
import logging
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

led_upper_pins = [12, 13, 14]
led_lower_pins = [15, 16, 17]
mcp = None  # MCP23017 GPIO Device for controlling the motors
mcp_address = 0x20
eta = 0


class Worker:

    def __init__(self, port, led_upper="#AAAAAA", led_lower="#AAAAAA"):
        global testing
        if not testing:
            self.init_motors()
        self.port = port
        self.led_upper = led_upper
        self.led_lower = led_lower
        self.current_drink = None

        server_address = ("localhost", port)
        httpd = HTTPServer(server_address, make_worker_server(self))
        logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
        logging.info("Serving at " + str(server_address))
        #httpd.serve_forever()

        self.thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        self.thread.start()

    def init_motors(self):
        logging.info("Initializing pump interface")
        global mcp
        global i2c
        mcp = MCP23017(i2c, address=mcp_address)
        mcp.iodir = 0
        mcp.gpio = 0xFFFF

    def get_led_upper(self):
        return self.led_upper

    def set_led_upper(self, value):
        self.led_upper = value
        # TODO: Actually write to GPIO
        return "Success!"

    def get_led_lower(self):
        return self.led_lower

    def set_led_lower(self, value):
        self.led_lower = value
        # TODO: Actually write to GPIO
        return "Success!"

    def activate_motor(self, address):
        if testing:
            logging.info("Simulated turning on " + str(address))
        else:
            mcp.get_pin(address).value = False

    def deactivate_motor(self, address):
        if testing:
            logging.info("Simulated turning off " + str(address))
        else:
            mcp.get_pin(address).value = True

    def timed_pour(self, address, delay):
        self.activate_motor(address)
        time.sleep(delay/1000)
        self.deactivate_motor(address)

    def complete_pour(self, threads):
        global eta
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        eta = 0
        logging.info("Pour complete!")

    def pour_drink(self, drink_json):
        """
        Handles the activation of motors and setting of drink array to stop specified motors when pour time has elapsed.
        :param drink : dict, Contains I2C Addresses (as Ints) and Pour times (in milliseconds) needed to pour specified drink.

        :return: int , ETA of drink being poured.
        """

        logging.info("Pouring a drink!!")
        logging.info(drink_json)
        drink = json.loads(drink_json)
        threads = []

        for ingredient in drink.keys():
            threads.append(threading.Thread(target=self.timed_pour, args=(ingredient, drink[ingredient])))
        threading.Thread(target=self.complete_pour, args=(threads,)).start()
        return eta

    @staticmethod
    def millis():
        return int(round(time.time() * 1000))


def make_worker_server(worker):
    class WorkerServer(BaseHTTPRequestHandler):

        def __init__(self, *args, **kwargs):
            self.worker = worker
            super(WorkerServer, self).__init__(*args, **kwargs)

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
                    response = str(self.worker.get_led_upper())
                elif target == "led_lower":
                    response = str(self.worker.get_led_lower())
                else:
                    response = "Invalid query!"
            elif "set" in query:
                target = query["set"][0]
                if target == "led_upper":
                    response = self.worker.set_led_upper(int(query["value"][0]))
                elif target == "led_lower":
                    response = self.worker.set_led_lower(int(query["value"][0]))
                else:
                    response = "Invalid query!"
            elif "drink" in query:
                try:
                    response = self.worker.pour_drink(query["drink"][0])
                except:
                    response = 0
            else:
                response = "Invalid Query!"

            self._set_headers()
            self.wfile.write(str(response).encode("utf8"))
    return WorkerServer

#def run():
#    print("running server")
#    if testing:
#        run_server()
#    else:
#        init_motors()
#        run_server()
