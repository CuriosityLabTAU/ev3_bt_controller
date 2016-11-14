from ev3_bt_controller import *
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
        self.m1_min, self.m1_max = rf.calibrate_motor(self.c, 1)
        rf.move2middle(self.m1_min, self.m1_max, self.c, 1)
        self.m2_min, self.m2_max = rf.calibrate_motor(self.c, 0)
        rf.move2middle(self.m2_min, self.m2_max, self.c, 0)
