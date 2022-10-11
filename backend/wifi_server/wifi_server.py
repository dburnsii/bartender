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
            self.nm_str = "org.freedesktop.NetworkManager"
            self.network_manager = self.system_bus.get(self.nm_str)
            for interface_str in self.network_manager.Devices:
                interface = self.system_bus.get(self.nm_str, interface_str)
                if interface.DeviceType == 2:
                    self.wifi_interface = interface
                    self.wifi_interface_path = interface_str

            if not self.wifi_interface:
                print("No wifi interface found!")
                exit(1)

            self.get_current_network()

            from gi.repository import GLib
            self.GLib = GLib
            self.loop = self.GLib.MainLoop()
            self.glib_thread = Thread(target=self.loop.run)
            self.glib_thread.start()

            self.wifi_interface.onAccessPointAdded = self.scan_update
            self.wifi_interface.onAccessPointRemoved = self.scan_update
            self.wifi_interface.onStateChanged = self.state_update
            print("Connecting via '{}'".format(self.wifi_interface.Interface))
        else:
            self.current_ssid = "Current Network"
            self.known_networks = ["Current Network"]
            self.available_networks = [
                {"name": "Current Network",
                 "signal": 80,
                 "auth": ['wpa-psk']},
                {"name": "Strongest Network",
                 "signal": 100,
                 "auth": ['wpa-psk']},
                {"name": "Weakest Network",
                 "signal": 20,
                 "auth": ['wpa-psk']},
                {"name": "Open Network",
                 "signal": 50,
                 "auth": ['']},
                {"name": "",
                 "signal": 50,
                 "auth": ['']},
                {"name": "EAP Network",
                 "signal": 50,
                 "auth": ['wpa-eap']}]

    def get_current_network(self):
        if not simulation:
            if self.wifi_interface.State == 100:
                current_bss_str = self.wifi_interface.ActiveAccessPoint
                self.current_ssid = \
                    self.convert_ssid(self.system_bus.get(self.nm_str,
                                                          current_bss_str).Ssid)
            else:
                self.current_ssid = ""
        self.sio.emit("wifi_current_ssid", {"ssid": self.current_ssid})
        print("Current network: '{}'".format(self.current_ssid))

    def get_known_networks(self):
        if not self.simulation:
            networks = []
            network_paths = self.wifi_interface.AvailableConnections
            for network_path in network_paths:
                network = self.system_bus.get(self.nm_str, network_path)
                settings = network.GetSettings()
                if settings["connection"]["type"] == "802-11-wireless":
                    networks.append(self.convert_ssid(settings["802-11-wireless"]["ssid"]))
            self.known_networks = networks
        self.sio.emit("wifi_known_network_results", {"networks": self.known_networks})
        print("Known networks: {}".format(self.known_networks))

    def run_scan(self):
        if not self.simulation:
            self.wifi_interface.onAccessPointAdded = self.scan_update
            self.wifi_interface.onAccessPointRemoved = self.scan_update
            self.wifi_interface.RequestScan({})
        else:
            self.scan_update(0)

    def scan_update(self, status):
        print("Scan results updated!")
        self.wifi_interface.onAccessPointAdded = None
        self.wifi_interface.onAccessPointRemoved = None
        if not self.simulation:
            self.available_networks = []
            for network_str in self.wifi_interface.AccessPoints:
                network = self.system_bus.get(self.nm_str, network_str)
                ssid = self.convert_ssid(network.Ssid)
                auth = network.RsnFlags
                signal = network.Strength
                self.available_networks.append({"name": ssid,
                                                "signal": signal,
                                                "auth": auth})
        self.sio.emit("wifi_scan_results",
                      {"networks": self.available_networks})
        self.get_current_network()
        print(self.available_networks)

    def connect(self, ssid, psk=None):
        print("Connecting to ssid: {}".format(ssid))
        if not self.simulation:
            connections = self.wifi_interface.AvailableConnections
            connection_found = False
            for connection in connections:
                c_settings = self.system_bus.get(self.nm_str,
                                                 connection).GetSettings()
                c_ssid = \
                    self.convert_ssid(c_settings["802-11-wireless"]["ssid"])
                if c_settings["connection"]["type"] == "802-11-wireless" and \
                   c_ssid == ssid:
                    self.network_manager.ActivateConnection(
                                                    connection,
                                                    self.wifi_interface_path,
                                                    self.get_network(ssid))
                    connection_found = True

            if not connection_found:
                output = self.network_manager.AddAndActivateConnection(
                                      {"802-11-wireless-security": {"psk": self.s(psk)}},
                                      self.wifi_interface_path,
                                      self.get_network(ssid))
            self.get_known_networks()
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
            self.system_bus.get(self.nm_str, self.get_connection(ssid)).Delete()
        self.get_known_networks()

    def state_update(self, arg1, arg2, arg3):
        print(arg1)
        print(arg2)
        print(arg3)
        self.get_current_network()

    def local_ip(self):
        return subprocess.check_output(["hostname", "-I"]).decode().strip()

    def get_network(self, ssid):
        for network_str in self.wifi_interface.AccessPoints:
            network = self.system_bus.get(self.nm_str, network_str)
            found_ssid = self.convert_ssid(network.Ssid)
            if found_ssid == ssid:
                return network_str

    def get_connection(self, ssid):
        if not self.simulation:
            networks = []
            network_paths = self.wifi_interface.AvailableConnections
            for network_path in network_paths:
                network = self.system_bus.get(self.nm_str, network_path)
                settings = network.GetSettings()
                if settings["connection"]["type"] == "802-11-wireless":
                    found_ssid = self.convert_ssid(settings["802-11-wireless"]["ssid"])
                    if found_ssid == ssid:
                        return network_path

    def s(self, string):
        return self.GLib.Variant("s", string)

    def convert_ssid(self, raw_ssid):
        return ''.join(map(lambda x: chr(x), raw_ssid))

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
    simulation = data["status"]
    print("Updating simulation status: {}".format(simulation))
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
