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
async def disconnect(sid):
    print('disconnect ', sid)
    for service in registered_services:
        if registered_services[service].sid == sid:
            print('{} Serivce was disconnected.'.format(service))
            del registered_services[service]
            await sio.emit('service_disconnected', {'name': service})
            break

@sio.on("*")
async def catch_all(event, sid, data):
    await sio.emit(event, data)


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
