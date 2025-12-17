# yaw_utils.py
from dronekit import VehicleMode
import math
import time

def condition_yaw(vehicle, heading, yaw_rate=5, relative=False):
    """
    Send MAV_CMD_CONDITION_YAW to the vehicle.

    Args:
        vehicle: DroneKit Vehicle object
        heading: degrees. If relative=True, amount to turn; else absolute heading
        yaw_rate: deg/s
        relative: bool, True = relative turn, False = absolute heading
    """
    if vehicle is None:
        print("Vehicle not connected")
        return

  
    is_relative = 1 if relative else 0

    # Default direction 0 = shortest path
    direction = 0

    # Send command
    vehicle.commands._master.mav.command_long_send(
        vehicle._master.target_system,
        vehicle._master.target_component,
        115,                  # MAV_CMD_CONDITION_YAW
        0,                    # confirmation
        heading,              # param1: yaw angle
        yaw_rate,             # param2: yaw rate deg/s
        direction,            # param3: direction (-1, 0, 1)
        is_relative,          # param4: relative/absolute
        0,0,0                 # param5-7 not used
    )

    # wait a short time for the yaw to start moving
    time.sleep(0.05)
