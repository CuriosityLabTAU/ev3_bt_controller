
import neuronets
from ev3_bt_controller import *
import robot_fun as rf
import numpy as np
import matplotlib.pyplot as plt

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
Nsteps = 100

nn1 = neuronets.NN(n1, p1, m1, eta1, eps1)
nn1.initialize_weights()

motors = [
    {
        'port': 1,
        'speed': 10,
        'duration': 1
    },
    {
        'port': 8,
        'speed': 0,
        'duration': 1
    }
]
c = EV3_BT_Controller(motors)


costLog = np.zeros((Nsteps, 1))
k = 0
for x in range(0,Nsteps):
    raw_a = np.random.randint(-100, high = 101)
    print(raw_a)
    motors = [
        {
            'port': 1,
            'speed': raw_a,
            'duration': 1
        },
        {
            'port': 8,
            'speed': 0,
            'duration': 1
        }
    ]
    print(motors)
    a_t0 = raw_a/motor_max
    raw_angles = c.get_degrees_two_motors(motors)
    raw_theta_t0 = raw_angles[0]
    theta_t0 = rf.map_angle(raw_theta_t0)
    c.move_two_motors(motors)
    raw_angles = c.get_degrees_two_motors(motors)
    raw_theta_t1 = raw_angles[0]
    theta_t1 = rf.map_angle(raw_theta_t1)
    x1 = [theta_t0, a_t0]
    d1 = theta_t1
    J = nn1.learnNew(x1, d1, eta1)
    costLog[k] = J
    k += 1

plt.plot(costLog)
plt.show()

