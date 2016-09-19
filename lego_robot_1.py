
import neuronets
from ev3_bt_controller import *
import robot_fun as rf
import numpy as np
import matplotlib.pyplot as plt

nInput = 2
nHidden = 10
nOut = 1
eta1 = 0.1
eps1 = 1
motor_max = 30
motor_min = -30
sensor_max = 360
sensor_min = 1
Nsteps = 10
resolution = 100

nn1 = neuronets.NN(nInput, nHidden, nOut, eta1, eps1)
nn1.initialize_weights()

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


costLog = np.zeros((Nsteps, 1))
k = 0
for x in range(0,Nsteps):
    raw_a = np.random.randint(motor_min, high = motor_max+1)
    print(raw_a)
    motors = [
        {
            'port': 1,
            'speed': 0,
            'duration': 1
        },
        {
            'port': 8,
            'speed': raw_a,
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
    xa, s1, za, s2, y = nn1.forProp(x1)
    J = nn1.backProp(xa, s1, za, s2, y, d1)
    costLog[k] = J
    k += 1

plt.figure(1)
plt.plot(costLog)

i1 = np.linspace(-1.0,1.0,resolution)
i2 = np.linspace(-1.0,1.0,resolution)
o1 = np.zeros((resolution, resolution))

for i in range (0, resolution):
    for j in range (0, resolution):
        print(j)
        x1 = [i1[i], i2[j]]
        xa, s1, za, s2, y = nn1.forProp(x1)
        o1[i, j] = y

X, Y = np.meshgrid(i1 ,i2)

plt.figure(2)
plt.contourf(X, Y, o1)
plt.show()

print(o1)
