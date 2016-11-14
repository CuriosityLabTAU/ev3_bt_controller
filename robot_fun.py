from ev3_bt_controller import *
import time


def map_angle(angle):
    angle_in_circle = angle % 360
    angle_symmetry = angle_in_circle - (360/2)
    angle_normal = angle_symmetry / (360/2)
    return angle_normal


def calibrate_motor(c, motor_num):

    print('starting calibration')

    c.motors[0]['speed'] = 0
    c.motors[1]['speed'] = 0

    calibration_speed = 10

    a = 1
    while a == 1:
        time.sleep(0.2)
        c.motors[motor_num]['speed'] = calibration_speed
        angles = c.get_degrees_two_motors(c.motors)
        old_angle = angles[motor_num]
        c.move_two_motors(c.motors)
        time.sleep(0.2)
        angles = c.get_degrees_two_motors(c.motors)
        print('old angle = ', old_angle, ' new angle =', angles[motor_num])
        if angles[motor_num] == old_angle :
            m1_max = old_angle
            a = 0

    a = 1
    while a == 1:
        time.sleep(0.)
        c.motors[motor_num]['speed'] = -calibration_speed
        angles = c.get_degrees_two_motors(c.motors)
        old_angle = angles[motor_num]
        c.move_two_motors(c.motors)
        time.sleep(0.2)
        angles = c.get_degrees_two_motors(c.motors)
        print('old angle = ', old_angle, ' new angle =', angles[motor_num])
        if angles[motor_num] == old_angle :
            m1_min = old_angle
            a = 0
    print("calibration done: max angle = ", m1_max, " min angle = ", m1_min)

    return m1_min, m1_max


def map2normal(raw_d, min_d, max_d):
    average = (max_d + min_d)/2
    amplitude = (max_d - min_d)/2
    mapped_d = (raw_d - average) / amplitude
    return mapped_d


def map_from_normal(raw_d, min_d, max_d):
    average = (max_d + min_d)/2
    amplitude = (max_d - min_d)/2
    mapped_d = raw_d * amplitude + average
    return mapped_d


def move2middle(m1_min, m1_max, c, motor_num) :
    c.motors[0]['speed'] = 0
    c.motors[1]['speed'] = 0
    angles = c.get_degrees_two_motors(c.motors)
    angle1 = angles[motor_num]
    middle = (m1_max + m1_min) / 2
    diff = 10
    while diff > 5:
        diff = angle1 - middle
        if diff > 0:
            v = -10
        else:
            v = 10
        c.motors[motor_num]['speed'] = v
        c.move_two_motors(c.motors)
    print('motor is centered')



