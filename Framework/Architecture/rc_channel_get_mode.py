# This program gives inputs to the guided_tracking.py to determine if the vehicle is controlled manually or autonomously.
from dronekit import connect
import time

# connect to ArduPilot
connection_string = "udp:127.0.0.1:14550"
print("Connecting to vehicle on:", connection_string)
vehicle = connect(connection_string, wait_ready=True, heartbeat_timeout=30)

def get_mode():
    # returns plane mode from ardupilot software
    return vehicle.mode.name



def read_rc_channel(ch):
  # This function will be used to know which channel is active. This means I can use the result to switch between autonomous and manned mode.
    """
    ch: integer channel number 1..12
    returns pwm value (us) or None if not present
    """
    ch_key = str(ch)
    if ch_key in vehicle.channels:
        return int(vehicle.channels[ch_key])
    else:
        return None

while True:
  mode = get_mode()
  ch7 = read_rc_channel(7)   # channel 7 is the tracking switch
  ch8 = read_rc_channel(8)   # channel 7 is the autonomous control switch
  ch9 = read_rc_channel(9)   # channel 9 is the manned control switch
  print(f"Mode: {mode}, CH7: {ch7}, CH8: {ch8}")
  time.sleep(0.5)
