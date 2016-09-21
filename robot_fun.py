from ev3_bt_controller import *
import time


def map_angle(angle):
    angle_in_circle = angle % 360
    angle_symmetry = angle_in_circle - (360/2)
    angle_normal = angle_symmetry / (360/2)
    return angle_normal


def calibrate_motor(c):

    calibration_speed = 10

    a = 1
    while (a == 1) :
        time.sleep(1.5)
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
        #print(angles)
        old_angle = angles[1]
        #print('old angle =')
        #print(old_angle)
        c.move_two_motors(motors)
        time.sleep(1.5)
        angles = c.get_degrees_two_motors(motors)
        print('old angle = ', old_angle, ' new angle =', angles[1])
        #print(angles[1])
        if angles[1] == old_angle :
            m1_max = old_angle
            a = 0

    a = 1

    while (a == 1) :
        time.sleep(1.5)
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
        #print(angles)
        old_angle = angles[1]
        #print('old angle =')
        #print(old_angle)
        c.move_two_motors(motors)
        time.sleep(1.5)
        angles = c.get_degrees_two_motors(motors)
        print('old angle = ', old_angle, ' new angle =', angles[1])
        #print('new angle =')
        #print(angles[1])
        if angles[1] == old_angle :
            m1_min = old_angle
            a = 0
    print("calibration done: max angle = ", m1_max, " min angle = ", m1_min)

    return m1_min, m1_max

def map2normal(raw_d, min_d, max_d):
    average  = (max_d + min_d)/2
    amplitude = (max_d - min_d)/2
    mapped_d = (raw_d - average) / amplitude
    return mapped_d

def map_from_normal(raw_d, min_d, max_d):
    average  = (max_d + min_d)/2
    amplitude = (max_d - min_d)/2
    mapped_d = raw_d * amplitude + average
    return mapped_d

def move2middle(m1_min, m1_max, c, motors) :
    angles = c.get_degrees_two_motors(motors)
    angle1 = angles[1]
    middle = (m1_max + m1_min) / 2
    diff = 10
    while diff > 5 :
        diff = angle1 - middle
        if diff > 0 :
            v = -10
        else :
            v = 10
        motors = [
        {
            'port': 1,
            'speed': 0,
            'duration': 1
        },
        {
            'port': 8,
            'speed': v,
            'duration': 0.01
        }
        ]
        c.move_two_motors(motors)
    print('motor is centered')



