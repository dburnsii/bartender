import serial, time, json

s = serial.Serial("/dev/ttyACM0", 19200, timeout=2)
# Allow Arduino to reset due to new connection
time.sleep(2)
print("Serial port ready!")

#s.write((json.dumps({"command": "highlight", "locations": [128]}) + "\x00").encode())
#print(s.read(64).decode())

#while True:
#  for i in range(0, 10, 1):
#    s.write((json.dumps({"command": "highlight", "locations": [i]}) + "\x00").encode())
    #print(i)
#    time.sleep(1)
#  for i in range(8, -1, -1):
#    s.write((json.dumps({"command": "highlight", "locations": [i]}) + "\x00").encode())
    #print(i)
#    time.sleep(1)
s.write((json.dumps({"command": "flow"}) + "\x00").encode())
#  time.sleep(10)
  #loc = int(input("location > "))
  #s.write((json.dumps({"command": "highlight", "locations": [loc, loc - 3000, loc + 3000]}) + "\x00").encode())
