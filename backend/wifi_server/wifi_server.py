#!/usr/bin/python3

import time
import json
import socketio
from datetime import datetime, timedelta
from threading import Thread
import subprocess

class WiFiServer:
    def __init__(self, sio, simulaton=True):
        self.simulation = simulation
        self.available_networks = []
        self.sio = sio

        if not self.simulation:
            from pydbus import SystemBus
            self.system_bus = SystemBus()
            self.supplicant_str = "fi.w1.wpa_supplicant1"
            self.wpa_supplicant = self.system_bus.get(self.supplicant_str)
            for interface_str in self.wpa_supplicant.Interfaces:
                interface = self.system_bus.get(self.supplicant_str, interface_str)
                if interface.Ifname == "wlan0":
                    self.wifi_interface = interface

            if not self.wifi_interface:
                print("No wifi interface found!")
                exit(1)

            self.get_current_network()

            from gi.repository import GLib
            self.loop = GLib.MainLoop()
            self.glib_thread = Thread(target=loop.run)
            self.glib_thread.start()

            self.wifi_interface.onScanDone = self.scan_done
            print("Connected via '{}'".format(self.wifi_interface.Ifname))

    def get_current_network(self):
        if simulation:
            self.current_ssid = "Current Network"
        elif self.wifi_interface.State == "completed":
            current_bss_str = self.wifi_interface.CurrentBSS
            self.current_ssid = \
                self.system_bus.get(self.supplicant_str, current_bss_str).SSID
        else:
            self.current_ssid = ""
        self.sio.emit("wifi_current_ssid", {"ssid": self.current_ssid})
        print("Current network: '{}'".format(self.current_ssid))


    def run_scan(self):
        if not self.simulation:
            self.wifi_interface.Scan({"Type": GLib.Variant("s", "active")})
        else:
            self.scan_done(0)

    def scan_done(self, status):
        print("Scan done!")
        self.available_networks = []
        if not self.simulation:
            for network_str in self.wifi_interface.BSSs:
                network = self.system_bus.get(self.supplicant_str, network_str)
                ssid = ''.join(map(lambda x: chr(x), network.SSID))
                auth = network.RSN['KeyMgmt']
                signal = network.Signal
                print("{} - {} - {}".format(ssid, signal, auth))
                self.available_networks.append({"name": ssid, "signal": signal, "auth": auth})
        else:
            self.available_networks = [
                {"name": "Current Network",
                 "signal": -35,
                 "auth": ['wpa-psk']},
                {"name": "Strongest Network",
                 "signal": -30,
                 "auth": ['wpa-psk']},
                {"name": "Weakest Network",
                 "signal": -80,
                 "auth": ['wpa-psk']},
                {"name": "Open Network",
                 "signal": -60,
                 "auth": ['']},
                {"name": "",
                 "signal": -45,
                 "auth": ['']},
                {"name": "EAP Network",
                 "signal": -50,
                 "auth": ['wpa-eap']}
            ]
        self.sio.emit("wifi_scan_results",
                      {"networks": self.available_networks})
        self.get_current_network()
        print(self.available_networks)

    def local_ip(self):
        return subprocess.check_output(["hostname", "-I"]).decode().strip()


print("Starting WiFi Server.")

simulation = True

sio = socketio.Client()
sio.connect("http://localhost:8080")

@sio.event
def connect():
    print("Connected to socket server.")
    sio.emit("register", {"name": "wifi"})


@sio.event
def simulation(data):
    global simulation
    print("Updating simulation status.")
    simulation = data["status"]

    if not simulation:
        setup_wifi()

@sio.event
def disconnect():
    print("Disconnected from server.")
    exit(0)

@sio.event
def wifi_scan(data):
    wifi_interface.run_scan()

lastping = datetime.now()
lastloop = datetime.now()

wifi_interface = WiFiServer(sio)

wifi_interface.run_scan()

while 1:
    time.sleep(0.01)
    if(datetime.now() - lastping > timedelta(seconds=5)):
        lastping = datetime.now()
        sio.emit('ping', "")
