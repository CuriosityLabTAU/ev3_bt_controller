
import neuronets
from ev3_bt_controller import *
import robot_fun as rf
import numpy as np

n1 = 2
p1 = 10
m1 = 1
eta1 = 0.1
eps1 = 0.1
itera1 = 1
motor_max = 100
motor_min = -100
sensor_max = 360
sensor_min = 1
Nsteps = 20

nn1 = neuronets.NN(n1, p1, m1, eta1, eps1)
nn1.initialize_weights()



raw_a = np.random.randint(-100, high = 101)
print(raw_a)

motors = [
    {
        'port': 1,
        'speed': 10,
        'duration': 1
    }
]
a_t0 = raw_a/motor_max

c = EV3_BT_Controller(motors)
raw_theta_t0 = c.get_degree_single_motor(motors)
theta_t0 = rf.map_angle(raw_theta_0)
c.move_single_motor(motors)
raw_theta_t1 = c.get_degree_single_motor(motors)
theta_t1 = rf.map_angle(raw_theta_1)
x1 = [theta_t0, a_t0]
d1 = theta_t1
nn1.learn = (x1, d1, itera1, eps1)