#!/usr/bin/python3

import time
import json
import socketio
import sys
from datetime import datetime, timedelta

# TODO: Surround this with some conditional import logic
import apt
import apt.progress

class AcquireProgress(apt.progress.base.AcquireProgress):
    def status_change(self, pkg, percent, status):
        print("Update progress change: '{}' '{}' '{}'\n\r".format(pkg, percent, status))
        sio.emit("apt_update_progress", {'status': percent})

class InstallProgress(apt.progress.base.InstallProgress):
    def status_change(self, pkg, percent, status):
        print("Install progress change: '{}' '{}' '{}'\n\r".format(pkg, percent, status))
        print(percent)
        print(percent.__class__)
        sio.emit("apt_upgrade_progress", {'progress': percent})

print("Starting Admin Server.")

apt_cache = apt.Cache()
updates_available = []
update_requested = False
upgrade_requested = False

print("Loaded apt cache.")

simulation = True
sio = socketio.Client()

@sio.event
def apt_update(data):
    global update_requested
    update_requested = True

@sio.event
def apt_upgrade(data):
    global upgrade_requested
    upgrade_requested = True

@sio.event
def current_version(data):
    global apt_cache
    if 'bartender' in apt_cache:
        version = apt_cache['bartender'].installed.version
        print("Broadcasting Bartender version '{}'".format(version))
        sio.emit('software_version', {'bartender_deb': version})

@sio.event
def connect():
    print("Connected to socket server.")
    sio.emit("register", {"name": "admin"})

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
lastupdate = datetime.now()

while 1:
    time.sleep(0.01)
    if(datetime.now() - lastping > timedelta(seconds=5)):
        lastping = datetime.now()
        sio.emit('ping', "")
    if(datetime.now() - lastupdate > timedelta(hours=1)):
        lastupdate = datetime.now()
    if update_requested and apt_cache:
        print("Checking for updates")
        apt_cache.update(fetch_progress=AcquireProgress())
        apt_cache.open(None)

        updates_available = list(filter(lambda x: x.is_upgradable, apt_cache))
        print("Upgradable packages: {}".format(updates_available))
        sio.emit("apt_updates_available",
                 {'status': (len(updates_available) > 0)})
        update_requested = False
    if upgrade_requested and apt_cache:
        print("Running system upgrade.")
        apt_cache.upgrade()
        apt_cache.commit(install_progress=InstallProgress())
        sio.emit("apt_upgrade_progress", {'progress': 100.0})
        print("Upgrade complete!")
        upgrade_requested = False
