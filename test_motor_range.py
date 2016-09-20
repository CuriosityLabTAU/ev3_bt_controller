
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
raw_a = 2
while (a == 1) :
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
    raw_angles = c.get_degrees_two_motors(motors)
    print(raw_angles)
    old_angle = raw_angles[1]
    print('old angle =')
    print(old_angle)
    c.move_two_motors(motors)
    time.sleep(1)
    raw_angles = c.get_degrees_two_motors(motors)
    print('new angle =')
    print(raw_angles[1])
    if raw_angles[1] == old_angle :
        m1_max = old_angle
        a = 0

a = 1
raw_a = -2
while (a == 1) :
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
    raw_angles = c.get_degrees_two_motors(motors)
    print(raw_angles)
    old_angle = raw_angles[1]
    print('old angle =')
    print(old_angle)
    c.move_two_motors(motors)
    time.sleep(1)
    raw_angles = c.get_degrees_two_motors(motors)
    print('new angle =')
    print(raw_angles[1])
    if raw_angles[1] == old_angle :
        m1_min = old_angle
        a = 0
