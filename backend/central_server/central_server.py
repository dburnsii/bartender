#!/usr/bin/python3

from aiohttp import web
import socketio
import time
import os

sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)


class RegisteredService():
    def __init__(self, sid, name):
        self.sid = sid
        self.name = name
        self.time = time.gmtime()

    def feed(self):
        self.time = time.gmtime()

    def active(self):
        if time.mktime(time.gmtime()) - time.mktime(self.time) > 5:
            return False
        return True


#
# Scale Server
#

@sio.event
async def weight(sid, data):
    await sio.emit('weight', data)


@sio.event
async def cup_presence(sid, data):
    await sio.emit('cup_presence', data)


@sio.event
async def tare_scale(sid, data):
    await sio.emit('tare_scale', data)


@sio.event
async def simulated_pour(sid, data):
    await sio.emit('simulated_pour', data)


@sio.event
async def manual_pour_status(sid, data):
    await sio.emit('manual_pour_status', data)


@sio.event
async def manual_pour_init(sid, data):
    await sio.emit('manual_pour_init', data)

#
#  Valve Server
#


@sio.event
async def activate_valve(sid, data):
    print("Activate")
    await sio.emit('activate_valve', data)


@sio.event
async def measured_pour(sid, data):
    print("Measured pour not implemented.")


@sio.event
async def deactivate_valve(sid, data):
    print("Deactivate")
    await sio.emit('deactivate_valve', data)


@sio.event
async def deactivate_valves(sid, data):
    print("Deactivate all")
    await sio.emit('deactivate_valves', data)


@sio.event
async def drink_pour_active(sid, data):
    print("Drink pour state updated.")
    await sio.emit('drink_pour_active', data)


@sio.event
async def abort_pour(sid, data):
    print("Aborting pour.")
    await sio.emit('abort_pour', data)

#
# System server
#


@sio.event
async def screen_brightness(sid, data):
    await sio.emit('screen_brightness', data)


#
# Admin Server
#

@sio.event
async def apt_update(sid, data):
    await sio.emit('apt_update', data)


@sio.event
async def apt_upgrade(sid, data):
    await sio.emit('apt_upgrade', data)


@sio.event
async def apt_upgrade_progress(sid, data):
    await sio.emit('apt_upgrade_progress', data)


@sio.event
async def apt_updates_available(sid, data):
    await sio.emit('apt_updates_available', data)

#
# WiFi Server
#


@sio.event
async def wifi_current_ssid(sid, data):
    await sio.emit('wifi_current_ssid', data)


@sio.event
async def wifi_scan(sid, data):
    await sio.emit('wifi_scan', data)


@sio.event
async def wifi_scan_results(sid, data):
    await sio.emit('wifi_scan_results', data)


@sio.event
async def wifi_get_networks(sid, data):
    await sio.emit('wifi_get_networks', data)


@sio.event
async def wifi_known_network_results(sid, data):
    await sio.emit('wifi_known_network_results', data)


@sio.event
async def wifi_connect(sid, data):
    await sio.emit('wifi_connect', data)


@sio.event
async def wifi_disconnect(sid, data):
    await sio.emit('wifi_disconnect', data)


@sio.event
async def wifi_forget(sid, data):
    await sio.emit('wifi_forget', data)

#
#  Central Server Stuff
#


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
async def register(sid, data):
    print("Registration: ")
    print(data)
    service_name = data["name"]
    registered_services[service_name] = RegisteredService(sid, service_name)
    await sio.emit("simulation", {"status": simulation}, to=sid)


@sio.event
async def drink_pour(sid, data):
    print("Pouring drink {}".format(data["id"]))
    await sio.emit("drink_pour", data)


@sio.event
async def ping(sid, data):
    for service in registered_services:
        if registered_services[service].sid == sid:
            registered_services[service].feed()


@sio.event
async def active_services(sid, data):
    services = []
    for service in registered_services:
        if service.active():
            services.append(service.name)
    await sio.emit('active_services', {'service_list': services})


@sio.event
async def error(sid, data):
    await sio.emit("error", data)


@sio.event
async def clear_error(sid, data):
    await sio.emit("clear_error", data)


@sio.event
async def idle(sid, data):
    await sio.emit("idle", data)


@sio.event
async def manual_override(sid, data):
    await sio.emit("manual_override", data)


@sio.event
async def highlight_bottles(sid, data):
    await sio.emit("highlight_bottles", data)


@sio.event
async def disconnect(sid):
    print('disconnect ', sid)
    for service in registered_services:
        if registered_services[service].sid == sid:
            print('{} Serivce was disconnected.'.format(service))
            del registered_services[service]
            await sio.emit('service_disconnected', {'name': service})
            break


async def on_startup(app):
    if systemd:
        n = sdnotify.SystemdNotifier()
        n.notify("READY=1")
    print("Server started")


if __name__ == '__main__':
    print("Starting Central Server")

    systemd = os.path.exists("/usr/bin/systemd")
    if systemd:
        import sdnotify
    print("Using Systemd: {}".format(systemd))

    print("Initialized Async Server.")

    registered_services = {}

    # Assume if we're running on an ARM OS, and systemd is installed, we're
    # on real hardware.
    simulation = True
    if (os.uname()[4] in ["armv7l", "arm64", "aarch64"]) and systemd:
        simulation = False

    print("Starting server")
    app.on_startup.append(on_startup)
    web.run_app(app)
