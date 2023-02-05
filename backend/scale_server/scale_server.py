#!/usr/bin/env python3

import socketio
import time
import sys
import requests
from simulated_scale import Simulator

import gc
last_weight = time.time()


sio = socketio.Client()
connected = False
present = False
simulation = True
simulated_pour_status = False
weight = 0
measures = [0, 0, 0]
# TODO: Make this user selectable
# calibration = 222.23
calibration = 10000
cup_threshold = 30
bad_reads = 0
adc = None
adc_module = "simulation"  # One of: "hx711", "nau7802", or "simulation"
manual_target = 0
manual_start = 0
config_url = "http://localhost:5000/config/"


def cleanup():
    global adc
    global adc_module
    print("Cleanup")
    if not simulation:
        if adc_module == "hx711":
            GPIO.cleanup()
        elif adc_module == "nau7802":
            adc.cleanup()
    sio.disconnect()
    gc.collect()
    sys.exit()


def variance():
    return max(measures) - min(measures)


def get_config(key):
    r = requests.get(config_url + key)
    if r.ok:
        print(r.text)
        return r.text.strip().replace("\"", "")
    else:
        print("Error getting config: '{}'".format(key))
        return None

def set_config(key, value):
    r = requests.put(config_url + key, value)
    if r.ok:
        print("Successfully updated: {}".format(key))
    else:
        print("Failed to update config: {}".format(key))


@sio.event
def cup_presence_request(data):
    global present
    print("Broadcasting presence '{}'".format(present))
    sys.stdout.flush()
    sio.emit('cup_presence', {'present': present})


@sio.event
def manual_pour_init(data):
    global present
    global weight
    global manual_target
    global manual_start

    print("Received manual pour request: {}".format(data))
    # TODO: Leave this out until we can stabilize the cup detection. Might
    #       also be good to leave out for cleaning.
    # if not present:
    #    return
    manual_target = data['quantity']
    manual_start = weight


@sio.event
def weight_request():
    global weight
    sio.emit('weight', {'weight': weight})


@sio.event
def simulation(data):
    global simulation
    global adc
    global adc_module
    simulation = data['status']
    print(simulation)

    adc_module = get_config("scale_controller")

    print("Initializing hardware")
    if adc_module == "simulation":
        adc = Simulator()
    elif adc_module == "hx711":
        global GPIO
        global HX711
        import RPi.GPIO as GPIO
        from hx711 import HX711
        print("Initializing HX711")
        adc = HX711(6, 5)
        adc.set_reference_unit(1)
        adc.reset()
        adc.tare()
    elif adc_module == "nau7802":
        print("Initializing NAU7802")
        global NAU7802
        from nau7802 import NAU7802
        adc = NAU7802(gain=128)
    else:
        print("No valid module selected.")
        adc = Simulator()
    print("Scale ready!")


@sio.event
def simulated_pour(data):
    print("Detected simulated pour")
    global simulated_pour_status
    simulated_pour_status = data['status']


@sio.event
def tare_scale(data):
    print("Zeroing scale")
    global adc
    global present
    adc.reset()
    adc.tare()
    present = False
    cup_presence_request("")


@sio.event
def calibrate_scale(data):
    global adc
    global calibration
    global simulation
    print("Calibrate")
    if "weight" not in data:
        print("Missing known weight")
        return
    known_weight = data["weight"]
    if simulation:
        current_weight = 100
    else:
        current_weight = adc.get_weight(10)
    calibration = known_weight / current_weight
    print("New calibration value: {}".format(calibration))
    set_config("scale_calibration", str(calibration))


@sio.event
def disconnect():
    print("Disconnected...")
    sys.stdout.flush()
    global connected
    connected = False


@sio.event
def connect():
    print("Connected!")
    sys.stdout.flush()
    sio.emit("register", {"name": "scale"})

    global connected
    connected = True


if __name__ == "__main__":
    sio.connect('http://localhost:8080')

    calibration = int(get_config("scale_calibration"))
    if calibration is None:
        calibration = 100

    while 1:
        try:
            if not simulation and adc:
                starttime = time.time()
                val = adc.get_weight(3)
                weight = val / calibration

                # If the read from the scale happens in less than 3ms, this is
                # usually because we're not actually able to communicate
                # with the hx711 module. Report this to the rest of the system.
                readtime = (time.time() - starttime)*1000
                print("{:.1f}g - {}ms".format(weight, readtime))
                if (readtime < 3):
                    # Try to only notify the rest of the system every once in
                    # a while
                    print("Error reading scale.")
                    bad_reads += 1
                    if (bad_reads == 10):
                        bad_reads += 1
                        sio.emit("error", {"title": "Scale Not Responding",
                                 "text": ("Currently unable to get a read "
                                          "from the scale. Please make sure "
                                          "it's properly connected.")})
                    time.sleep(1)
                    continue
                else:
                    if (bad_reads > 0):
                        sio.emit("clear_error", {"title":
                                                 "Scale Not Responding"})
                    bad_reads = 0

                measures.append(weight)
                measures.pop(0)
                if (weight > cup_threshold and variance() < 5 and not present):
                    print("Cup detected")
                    present = True
                    cup_presence_request()
                    adc.tare()
                    continue
                elif (weight < (cup_threshold * -0.5) and
                      variance() < 5 and
                      present):
                    print("Cup removed")
                    present = False
                    cup_presence_request()
                    adc.tare()
                elif (manual_target > 0):
                    manual_percentage = (weight - manual_start) / manual_target
                    print("Manual percentage: {}".format(manual_percentage))
                    if (manual_percentage >= 1.0):
                        print("Manual pour complete!")
                        manual_target = 0
                        sio.emit('manual_pour_status', {
                                'percentage': manual_percentage,
                                'complete': True})
                    else:
                        sio.emit('manual_pour_status', {
                                'percentage': manual_percentage,
                                'complete': False})
                weight_request()
                time.sleep(0.05)
            elif connected:
                if simulated_pour_status:
                    if not present:
                        present = True
                        cup_presence_request()
                    weight += 2
                    if manual_target > 0:
                        manual_percentage = \
                            (weight - manual_start) / manual_target
                        print("Manual percentage: {}"
                              .format(manual_percentage))
                        if (manual_percentage >= 1.0):
                            print("Manual pour complete!")
                            manual_target = 0
                            sio.emit('manual_pour_status', {
                                'percentage': manual_percentage,
                                'complete': True})
                        else:
                            sio.emit('manual_pour_status', {
                                'percentage': manual_percentage,
                                'complete': False})
                else:
                    if present:
                        present = False
                        weight = 0
                        cup_presence_request()
                weight_request()
                time.sleep(0.1)
            else:
                print("Not connected...")
                # sio.connect('http://localhost:8080')
                time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            cleanup()
