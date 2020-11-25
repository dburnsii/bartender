#!/usr/bin/python3

simulation = True

import socketio
import atexit
import sys
import time
import utils

def cleanup():
    sio.disconnect()
    if not simulation:
        for pin in pins:
            gpio.setup(pin, gpio.OUT)
            gpio.output(pin, gpio.LOW)
        gpio.cleanup()

pins = [21, 20, 26, 16, 19, 13, 22, 22, 22, 22]
enable_pin = 27
enable_time = 0
pour_target = 0
pour_total = 0
pour_queue = []
scale_heartbeat = time.time()
scale_cache = []
scale_cache_size = 20
cup_presence_status = False
scale_failure_threshold = 5

sio = socketio.Client()

@sio.event
def activate_valve(data):
    global cup_presence_status
    print(data)
    print("Oh you want me to turn on  pump {}?".format(data['pin']))
    if not simulation:
        if cup_presence_status:
            gpio.output(pins[int(data['pin'])], gpio.HIGH)
            gpio.output(enable_pin, gpio.HIGH)
    else:
        print("Simulating pour on valve {}".format(data['pin']))
        sio.emit("simulated_pour", {"status": True})

@sio.event
def deactivate_valve(data):
    global enable_time
    print(data)
    print("Had enough of {} huh?".format(data['pin']))
    if not simulation:
        gpio.output(pins[int(data['pin'])], gpio.LOW)
        enable_time = time.time() + 1

@sio.event
def deactivate_valves(data=None):
    global simulation
    global enable_time
    print("Shutting off all valves.")
    if not simulation:
        for pin in pins:
            gpio.output(pin, gpio.LOW)
        enable_time = time.time() + 1
    else:
        sio.emit("simulated_pour", {"status": False})

@sio.event
def drink_pour(data):
    global pour_queue
    global pour_target
    global simulation
    global pour_total
    global scale_cache
    global cup_presence_status
    if(len(pour_queue)):
        print("Uh... we're  little busy...")
        sio.emit("error", {"title": "Pour in progress",
                           "text": "A drink is currently being poured. please"\
                                    "wait until the drink is complete before "\
                                    "beginning another pour."})
        return
    if not simulation and not cup_presence_status:
        print("Cup presence not detected. Aborting pour.")
        sio.emit("error", {"title": "Missing Cup",
                           "text": "No cup detected on the scale. Please place"\
                                    " a cup on the scale before pouring a drink."})
        return
    print(data)
    print("Pouring you a drank, oh-woah-we-woah")
    valves = utils.grab_valves()
    drink = utils.grab_drink(data["id"])
    print(drink)
    pour_queue = []
    pour_total = 0
    for ingredient in drink["ingredients"]:
        if not utils.ing_pourable(ingredient):
            print("Skipping non-pourable ingredient: {}".format(ingredient["ingredient"]))
        elif(utils.ing_available(ingredient, valves)):
            print("Found a loaded ingredient")
        elif(not ingredient["required"]):
            print("Skipping a non-required ingredient")
        else:
            print("{} not in {}".format(ingredient["ingredient"], valves))
            sio.emit("error",
                {"title": "Missing Ingredients",
                 "text": "Missing ingredient required \
                  to pour {}: {}"
                  .format(drink["name"], ingredient["ingredient"])})
            return
    print("Ready to pour!")
    (pour_queue, pour_total) = utils.create_drink_queue(drink["ingredients"], valves)
    first_ingredient = pour_queue.pop(0)
    pour_target = scale_cache[-1] + first_ingredient["quantity"]
    print("Pour target: {}".format(pour_target))
    sio.emit("drink_pour_active", {"status": True})
    if simulation:
        sio.emit("simulated_pour", {"status": True})
    else:
        sio.emit("activate_valve", {"pin": first_ingredient["pin"]})
    # Add a rouge value to trick the variance algorithm into thinking the pour has started
    if(len(scale_cache) > 100):
        scale_cache.pop(0)
    scale_cache.append(-100)

@sio.event
def abort_pour(data):
    global pour_target
    global pour_queue
    deactivate_valves()
    pour_target = 0
    pour_queue = []
    sio.emit("drink_pour_active", {"status": False, "progress": 0})

@sio.event
def weight(data):
    global scale_cache
    global scale_heartbeat
    global pour_queue
    global pour_target
    global pour_total
    global scale_cache_size

    # Cache the recent scale values for no-progress detection
    scale_cache.append(data["weight"])
    if(len(scale_cache) > scale_cache_size):
        scale_cache.pop(0)
    scale_heartbeat = time.time()
    #print(utils.variance(scale_cache))

    # Check if we finished pouring our last ingredient
    if pour_target > 0:
        if utils.variance(scale_cache) < scale_failure_threshold:
            print("Minimum variance detected on scale. Aborting pour. Check to make sure bottle is connected and flowing.")
            abort_pour("")
            return
        if scale_cache[-1] >= pour_target:
            print("Ingredient target reached!")
            deactivate_valves()
            pour_target = 0
            if(len(pour_queue)):
                print(pour_queue)
                ingredient = pour_queue.pop(0)
                pour_target = scale_cache[-1] + ingredient["quantity"]
                print("Pour target: {}".format(pour_target))
                sio.emit("drink_pour_active", {"status": True})
                sio.emit("activate_valve", {"pin": ingredient["pin"]})
            else:
                print("Finished pouring drink!")
                sio.emit("drink_pour_active", {"status": False, "progress": 0})
        else:
            remaining_total = utils.remaining_in_queue(pour_queue)
            remaining_current = pour_target - scale_cache[-1]
            progress = (pour_total - (remaining_current + remaining_total)) / (pour_total) * 100
            sio.emit("drink_pour_active", {"status": True, "progress": progress})

@sio.event
def cup_presence(data):
    global cup_presence_status
    cup_presence_status = data["present"]


@sio.event
def connect():
    print("Connected to socket server.")
    sio.emit("register", {"name": "valve"})
    sio.emit("cup_presence_request", {})

@sio.event
def simulation(data):
    global simulation
    print("Updating simulation status.")
    simulation = data["status"]

    if not simulation:
        global gpio
        import RPi.GPIO as gpio
        gpio.setmode(gpio.BCM)
        for pin in pins:
            gpio.setup(pin, gpio.OUT)
            gpio.output(pin, gpio.LOW)
        gpio.setup(enable_pin, gpio.OUT)
        gpio.output(enable_pin, gpio.LOW)

@sio.event
def disconnect():
    print("Disconnected from server. Shutting off all pumps.")
    if not simulation:
        for pin in pins:
            gpio.output(pin, gpio.LOW)
        gpio.output(enable_pin, gpio.LOW)
    sys.exit(0)

sio.connect("http://localhost:8080")

while 1:
    time.sleep(0.25)
    sio.emit("ping", "")
    if(enable_time > 0 and time.time() > enable_time):
        gpio.output(enable_pin, gpio.LOW)
        enable_time = 0
    if(time.time() - scale_heartbeat > 3):
        print("ERROR! Scale has no pulse! Shutting all valves off as a safety measure")
        deactivate_valves()
        pour_target = 0
        pour_queue = []