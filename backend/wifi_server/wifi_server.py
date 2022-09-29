#!/usr/bin/python3

import time
import json
import socketio
from datetime import datetime, timedelta
from threading import Thread
import subprocess

class WiFiServer:
    def __init__(self, sio, simulation=True):
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
            self.GLib = GLib
            self.loop = self.GLib.MainLoop()
            self.glib_thread = Thread(target=self.loop.run)
            self.glib_thread.start()

            self.wifi_interface.onScanDone = self.scan_done
            print("Connected via '{}'".format(self.wifi_interface.Ifname))
        else:
            self.current_ssid = "Current Network"
            self.known_networks = ["Current Network"]
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
                 "auth": ['wpa-eap']}]

    def get_current_network(self):
        if not simulation:
            if self.wifi_interface.State == "completed":
                current_bss_str = self.wifi_interface.CurrentBSS
                self.current_ssid = \
                    self.system_bus.get(self.supplicant_str,
                                        current_bss_str).SSID
            else:
                self.current_ssid = ""
        self.sio.emit("wifi_current_ssid", {"ssid": self.current_ssid})
        print("Current network: '{}'".format(self.current_ssid))

    def get_known_networks(self):
        if not self.simulation:
            networks = []
            network_paths = self.wifi_interface.Networks
            for network_path in network_paths:
                network = self.system_bus.get(self.supplicant_str, network_path)
                networks.append(network.Properties['ssid'])
            self.known_networks = networks
        self.sio.emit("wifi_known_network_results", {"networks": self.known_networks})
        print("Known networks: {}".format(self.known_networks))

    def run_scan(self):
        if not self.simulation:
            self.wifi_interface.Scan({"Type": self.GLib.Variant("s", "active")})
        else:
            self.scan_done(0)

    def scan_done(self, status):
        print("Scan done!")
        if not self.simulation:
            self.available_networks = []
            for network_str in self.wifi_interface.BSSs:
                network = self.system_bus.get(self.supplicant_str, network_str)
                ssid = ''.join(map(lambda x: chr(x), network.SSID))
                auth = network.RSN['KeyMgmt']
                signal = network.Signal
                print("{} - {} - {}".format(ssid, signal, auth))
                self.available_networks.append({"name": ssid, "signal": signal, "auth": auth})
        self.sio.emit("wifi_scan_results",
                      {"networks": self.available_networks})
        self.get_current_network()
        print(self.available_networks)

    def connect(self, ssid, psk=None):
        print("Connecting to ssid: {}".format(ssid))
        if not self.simulation:
            # TODO: Check if there network exists already. If not, create it.
            pass
        else:
            if ssid in self.known_networks:
                self.current_ssid = ssid
            else:
                if psk == "Password!":
                    print("Password good! Connecting.")
                    self.known_networks.append(ssid)
                    self.current_ssid = ssid
                else:
                    print("Incorrect password.")
                    # TODO: error handling for bad password
                    pass
        self.sio.emit("wifi_current_ssid", {"ssid": self.current_ssid})


    def disconnect(self):
        if not self.simulation:
            self.wifi_interface.Disconnect()
        self.current_ssid = ""
        self.sio.emit("wifi_current_ssid", {"ssid": self.current_ssid})

    def forget(self, ssid):
        print("Forgetting ssid: {}".format(ssid))
        if self.current_ssid == ssid:
            self.disconnect()
        if simulation:
            if ssid in self.known_networks:
                self.known_networks.remove(ssid)
        else:
            # TODO: Remove network
            pass
        self.get_known_networks()

    def local_ip(self):
        return subprocess.check_output(["hostname", "-I"]).decode().strip()


print("Starting WiFi Server.")

simulation = True

sio = socketio.Client()
wifi_interface = None

@sio.event
def connect():
    print("Connected to socket server.")
    sio.emit("register", {"name": "wifi"})


@sio.event
def simulation(data):
    global simulation
    global wifi_interface
    print("Updating simulation status.")
    simulation = data["status"]
    wifi_interface = WiFiServer(sio, simulation=simulation)
    wifi_interface.run_scan()


@sio.event
def disconnect():
    print("Disconnected from server.")
    exit(0)

@sio.event
def wifi_scan(data):
    wifi_interface.run_scan()

@sio.event
def wifi_get_networks(data):
    wifi_interface.get_known_networks()

@sio.event
def wifi_connect(data):
    if 'password' in data:
        wifi_interface.connect(data['name'], data['password'])
    else:
        wifi_interface.connect(data['name'])

@sio.event
def wifi_disconnect(data):
    wifi_interface.disconnect()

@sio.event
def wifi_forget(data):
    wifi_interface.forget(data['name'])

sio.connect("http://localhost:8080")

lastping = datetime.now()
lastloop = datetime.now()


while 1:
    time.sleep(0.01)
    if(datetime.now() - lastping > timedelta(seconds=5)):
        lastping = datetime.now()
        sio.emit('ping', "")
