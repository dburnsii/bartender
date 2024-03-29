#!/usr/bin/python3

import utils
import time
import sys
import atexit
import socketio
import requests


controller = None
controller_type = "simulation"  # One of: simulation, gpio, mcp23017
pour_target = 0
pour_total = 0
pour_queue = []
scale_heartbeat = time.time()
scale_cache = []
scale_cache_size = 20
cup_presence_status = False
scale_failure_threshold = 5
manual_override = False
manual_pour_active = False

sio = socketio.Client()


@atexit.register
def cleanup():
    sio.disconnect()
    if not simulation:
        for pin in pins:
            gpio.setup(pin, gpio.OUT)
            gpio.output(pin, gpio.LOW)
        gpio.cleanup()


def get_config(key):
    r = requests.get(config_url + key)
    if r.ok:
        print(r.text)
        return r.text.strip().replace("\"", "")
    else:
        print("Error getting config: '{}'".format(key))
        return None


@sio.event
def activate_valve(data):
    global cup_presence_status
    global controller
    global manual_override

    print("Activating Valve: {}".format(data['pin']))
    if cup_presence_status or manual_override:
        controller.activate(int(data['pin']))


@sio.event
def deactivate_valve(data):
    print("Deactivating Valve: {}".format(data['pin']))
    # As of right now, we can only allow one valve to operate
    # at a time, due to the scale constraints. If this is
    # overcome, this may resume deactivating single valves,
    # but until then, it doesn't hurt to make sure all valves
    # are turned off.
    deactivate_valves()


@sio.event
def deactivate_valves(data=None):
    print("Shutting off all valves.")
    for pin in range(controller.count):
        controller.deactivate(pin)


@sio.event
def drink_pour(data):
    global pour_queue
    global pour_target
    global simulation
    global pour_total
    global scale_cache
    global cup_presence_status
    if (len(pour_queue)):
        print("Uh... we're  little busy...")
        sio.emit("error", {"title": "Pour in progress",
                           "text": "A drink is currently being poured. please"
                                    "wait until the drink is complete before "
                                    "beginning another pour."})
        return
    if not simulation and not cup_presence_status:
        print("Cup presence not detected. Aborting pour.")
        sio.emit("error", {"title": "Missing Cup",
                           "text": "No cup detected on the scale. Please "
                                   "place a cup on the scale before pouring a "
                                   "drink."})
        return

    print("Pouring you a drank, oh-woah-we-woah")
    valves = utils.grab_valves()
    drink = utils.grab_drink(data["id"])
    pour_queue = []
    pour_total = 0
    for ingredient in drink["ingredients"]:
        if not utils.ing_pourable(ingredient):
            print("Skipping non-pourable ingredient: {}".
                  format(ingredient["ingredient"]))
        elif (utils.ing_available(ingredient, valves)):
            print("Found a loaded ingredient")
        elif (not ingredient["required"]):
            print("Skipping a non-required ingredient")
        else:
            print("{} not in {}".format(ingredient["ingredient"], valves))
            sio.emit("error",
                     {"title": "Missing Ingredients",
                      "text": "Missing ingredient required "
                              "to pour {}: {}"
                      .format(drink["name"], ingredient["ingredient"])})
            return
    print("Ready to pour!")
    (pour_queue, pour_total) = utils.create_drink_queue(
        drink["ingredients"], valves)
    first_ingredient = pour_queue.pop(0)
    pour_target = scale_cache[-1] + first_ingredient["quantity"]
    print("Pour target: {}".format(pour_target))
    sio.emit("drink_pour_active", {"status": True})
    controller.activate(first_ingredient["pin"])
    # Add a rouge value to trick the variance algorithm into thinking the pour
    # has started
    if (len(scale_cache) > 100):
        scale_cache.pop(0)
    scale_cache.append(-100)


@sio.event
def abort_pour(data):
    global pour_target
    global pour_queue
    global manual_pour_active
    deactivate_valves()
    pour_target = 0
    pour_queue = []
    manual_pour_active = False
    sio.emit("drink_pour_active", {"status": False, "progress": 0})
    sio.emit("manual_pour_status", {"complete": True, "progress": 0})


@sio.event
def manual_pour_status(data):
    global manual_pour_active
    if data['complete']:
        manual_pour_active = False


@sio.event
def weight(data):
    global scale_cache
    global scale_heartbeat
    global pour_queue
    global pour_target
    global pour_total
    global scale_cache_size
    global manual_pour_active

    # Cache the recent scale values for no-progress detection
    scale_cache.append(data["weight"])
    if (len(scale_cache) > scale_cache_size):
        scale_cache.pop(0)
    scale_heartbeat = time.time()

    # Check if we finished pouring our last ingredient
    if pour_target > 0:
        if (manual_pour_active is False and
           utils.variance(scale_cache) < scale_failure_threshold):
            print("Minimum variance detected on scale. Aborting pour. "
                  "Check to make sure bottle is connected and flowing.")
            abort_pour("")
            return
        if scale_cache[-1] >= pour_target:
            print("Ingredient target reached!")
            deactivate_valves()
            pour_target = 0
            if (len(pour_queue)):
                print(pour_queue)
                ingredient = pour_queue.pop(0)
                pour_target = scale_cache[-1] + ingredient["quantity"]
                print("Pour target: {}".format(pour_target))
                sio.emit("drink_pour_active", {"status": True})
                if ingredient["pin"] is None:
                    print("Kick off manual pour!")
                    manual_pour_active = True
                    sio.emit("manual_pour_init", {
                        "name": ingredient["name"],
                        "quantity": ingredient["quantity"]})
                    sio.emit("simulated_pour", {"status": True})
                else:
                    controller.activate(ingredient["pin"])
            else:
                print("Finished pouring drink!")
                sio.emit("drink_pour_active", {"status": False, "progress": 0})
        else:
            remaining_total = utils.remaining_in_queue(pour_queue)
            remaining_current = pour_target - scale_cache[-1]
            progress = (pour_total - (remaining_current +
                        remaining_total)) / (pour_total) * 100
            sio.emit("drink_pour_active", {
                     "status": True, "progress": progress})


@sio.event
def cup_presence(data):
    global cup_presence_status
    cup_presence_status = data["present"]


@sio.event
def manual_override(data):
    global manual_override
    manual_override = data["status"]


@sio.event
def connect():
    print("Connected to socket server.")
    sio.emit("register", {"name": "valve"})
    sio.emit("cup_presence_request", {})


@sio.event
def simulation(data):
    global controller_type
    global controller
    print("Updating simulation status.")
    simulation = data["status"]

    controller_type = get_config("valve_controller")

    if controller_type == "gpio":
        from gpio import GpioController
        controller = GpioController()
    elif controller_type == "mcp23017":
        from mcp23017 import McpController
        controller = GpioController()
    elif controller_type == "pcal6416a":
        from pcal6416a import GpioController
        controller = GpioController()
    else:
        from sim_controller import SimulationController
        controller = SimulationController()
        controller.init_socket(sio)


@sio.event
def disconnect():
    print("Disconnected from server. Shutting off all pumps.")
    controller.cleanup()
    sys.exit(0)


sio.connect("http://localhost:8080")

while 1:
    time.sleep(0.25)
    sio.emit("ping", "")
    if (time.time() - scale_heartbeat > 3):
        if not manual_override:
            print("ERROR! Scale has no pulse! Shutting all valves off as a "
                  "safety measure")
            deactivate_valves()
            cup_presence_status = False
            pour_target = 0
            pour_queue = []
