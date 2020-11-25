#!/usr/bin/python3
import socketio
import time
import sys


sio = socketio.Client()
connected = False
present = False
simulation = True
simulated_pour_status = False
weight = 0
measures = [0,0,0]
#calibration = 394.5
calibration = 222.23
cup_threshold = 30
bad_reads = 0
hx = None

def cleanup():
    print("Cleanup")
    if not simulation:
        GPIO.cleanup()
    sio.disconnect()
    sys.exit()

def variance():
    return max(measures) - min(measures)

@sio.event
def cup_presence_request():
    global present
    print("Broadcasting presence '{}'".format(present))
    sys.stdout.flush()
    sio.emit('cup_presence', {'present': present})

@sio.event
def weight_request():
    global weight
    sio.emit('weight', {'weight': weight})

@sio.event
def simulation(data):
    global simulation
    simulation = data['status']

    if not simulation:
        print("Initializing hardware")
        global GPIO
        global HX711
        global hx
        import RPi.GPIO as GPIO
        from hx711 import HX711

        print("Initializing scale")
        hx = HX711(5,6)
        hx.set_reference_unit(1)
        hx.reset()
        hx.tare()
        print("Scale ready!")

@sio.event
def simulated_pour(data):
    global simulated_pour_status
    simulated_pour_status = data['status']

@sio.event
def tare_scale(data):
    print("Zeroing scale")
    global hx
    global present
    hx.reset()
    hx.tare()
    present = False
    cup_presence_request()

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

sio.connect('http://localhost:8080')
while 1:
    try:
        if not simulation and hx:
            starttime = time.time()
            val = hx.get_weight(3)
            weight = val / calibration

            # If the read from the scale happens in less than 3ms, this is usually because we're not actually able to communicate
            # with the hx711 module. Report this to the rest of the system.
            readtime = (time.time() - starttime)*1000
            print("{:.1f}g - {}ms".format(weight,readtime))
            if(readtime < 3):
                # Try to only notify the rest of the system every once in a while
                print("Error reading scale.")
                bad_reads += 1
                if(bad_reads == 10):
                    bad_reads += 1
                    sio.emit("error", {"title": "Scale Not Responding", "text": "Currently unable to get a read from the scale. Please make sure it's properly connected."})
                time.sleep(1)
                continue
            else:
                if(bad_reads > 0):
                    sio.emit("clear_error", {"title": "Scale Not Responding"})
                bad_reads = 0

            measures.append(weight)
            measures.pop(0)
            if(weight > cup_threshold and variance() < 5 and not present):
                print("Cup detected")
                present = True
                cup_presence_request()
                hx.tare()
                continue
            elif(weight < (cup_threshold * -0.5) and variance() < 5 and present):
                print("Cup removed")
                present = False
                cup_presence_request()
                hx.tare()
            weight_request()
            time.sleep(0.25)
        elif connected:
            if simulated_pour_status:
                if not present:
                    present = True
                    cup_presence_request()
                weight += 5
            else:
                if present:
                    present = False
                    weight = 0
                    cup_presence_request()
            weight_request()
            time.sleep(0.5)
        else:
            print("Not connected...")
            #sio.connect('http://localhost:8080')
            time.sleep(1)


    except (KeyboardInterrupt, SystemExit):
        cleanup()
