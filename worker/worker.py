#!/usr/bin/python

import json
import importlib
from http.server import HTTPServer, BaseHTTPRequestHandler


smbus_lib = importlib.util.find_spec('smbus')
gpio_lib = importlib.util.find_spec('RPi')

if smbus_lib is None or gpio_lib is None:
    testing = True
else:
    testing = False
    import smbus
    import RPi.GPIO as GPIO

PORT = 8080

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        return "test!".encode("utf8")

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("test"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.wfile.write(self._html("Post"))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=PORT):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print("Serving")
    httpd.serve_forever()


run()
