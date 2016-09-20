from ev3_bt_controller import *
import time


def map_angle(angle):
    angle_in_circle = angle % 360
    angle_symmetry = angle_in_circle - (360/2)
    angle_normal = angle_symmetry / (360/2)
    return angle_normal


def calibrate_motor(motors, c):

    calibration_speed = 2

    a = 1
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
            'speed': calibration_speed,
            'duration': 0.02
        }
        ]
        angles = c.get_degrees_two_motors(motors)
        print(angles)
        old_angle = angles[1]
        print('old angle =')
        print(old_angle)
        c.move_two_motors(motors)
        time.sleep(1)
        angles = c.get_degrees_two_motors(motors)
        print('new angle =')
        print(angles[1])
        if angles[1] == old_angle :
            m1_max = old_angle
            a = 0

    a = 1

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
            'speed': -calibration_speed,
            'duration': 0.02
        }
        ]
        angles = c.get_degrees_two_motors(motors)
        print(angles)
        old_angle = angles[1]
        print('old angle =')
        print(old_angle)
        c.move_two_motors(motors)
        time.sleep(1)
        angles = c.get_degrees_two_motors(motors)
        print('new angle =')
        print(angles[1])
        if angles[1] == old_angle :
            m1_min = old_angle
            a = 0

    return m1_min, m1_max
