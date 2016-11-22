from ev3_bt_controller import *
from camera import *
import robot_fun as rf
import numpy as np
import time
import math

class Robot:
    def __init__(self):
        self.motor_min = -30
        self.motor_max = 30
        self.safety_margin = 21
        self.c = EV3_BT_Controller()
        self.img = Camera(0.05)
        self.img.show_video()
        self.m1_min, self.m1_max = rf.calibrate_motor(self.c, 1)
        rf.move2middle(self.m1_min, self.m1_max, self.c, 1)
        self.m2_min, self.m2_max = rf.calibrate_motor(self.c, 0)
        rf.move2middle(self.m2_min, self.m2_max, self.c, 0)

    def command_motors(self, a1, a2):
        current_Angles = self.c.get_degrees_two_motors(self.c.motors)
        raw_p1_t0 = current_Angles[1]
        raw_p2_t0 = current_Angles[0]
        p1_t0 = rf.map2normal(raw_p1_t0, self.m1_min, self.m1_max)
        p2_t0 = rf.map2normal(raw_p2_t0, self.m2_min, self.m2_max)
        if current_Angles[1]-self.m1_min < self.safety_margin and a1 < 0:
            a1 = 0
        if self.m1_max - current_Angles[1] < self.safety_margin and a1 > 0:
            a1 = 0
        if current_Angles[0]-self.m2_min < self.safety_margin and a2 < 0:
            a2 = 0
        if self.m2_max - current_Angles[0] < self.safety_margin and a2 > 0:
            a2 = 0
        A1 = int(rf.map_from_normal(a1, self.motor_min, self.motor_max))
        A2 = int(rf.map_from_normal(a2, self.motor_min, self.motor_max))
        motors = [
            {
                'port': 1,
                'speed': A2,
                'duration': 0.1
            },
            {
                'port': 8,
                'speed': A1,
                'duration': 0.1
            }
        ]
        self.c.move_two_motors(motors)

    def read_motor_sensors(self):
        motors = self.c.motors
        Angles = self.c.get_degrees_two_motors(motors)
        p1_t0 = rf.map2normal(Angles[0], self.m1_min, self.m1_max)
        p2_t0 = rf.map2normal(Angles[1], self.m2_min, self.m2_max)
        angles = [p1_t0, p2_t0]
        return angles

    def get_image(self):
        image = np.interp(self.img.res,[0,256],[-1,1])
        return image

