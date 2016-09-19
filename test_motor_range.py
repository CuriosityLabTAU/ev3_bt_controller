
import neuronets
from ev3_bt_controller import *
import robot_fun as rf
import numpy as np
import matplotlib.pyplot as plt
import time


motors = [
    {
        'port': 1,
        'speed': 0,
        'duration': 1
    },
    {
        'port': 8,
        'speed': 0,
        'duration': 1
    }
]
c = EV3_BT_Controller(motors)

a = 1
raw_a = 10
while (a == 1) :
    raw_angles = c.get_degrees_two_motors(motors)
    print(raw_angles)
    time.sleep(1)
    motors = [
    {
        'port': 1,
        'speed': 0,
        'duration': 1
    },
    {
        'port': 8,
        'speed': raw_a,
        'duration': 0.02
    }
    ]
    #c.move_two_motors(motors)