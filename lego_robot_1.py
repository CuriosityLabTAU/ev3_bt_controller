
import neuronets
from ev3_bt_controller import *
import robot_fun as rf
import numpy as np
import matplotlib.pyplot as plt
import time
import math


np.random.seed(1)
nInput = 2
nHidden = 10
nOut = 1

eta1 = 0.01
eps1 = 1
pruning_rate = 0.0001
pruning_thresh = 0.05
motor_max = 30
motor_min = -30
sensor_max = 360
sensor_min = 1
Nsteps = 200
resolution = 100
safety_margin = 21

N_motors = 2  # number of motors
N_elements = N_motors * 3  # each motor has three elements - p(t), p(t+1), a(t)
N = N_elements
N_nets = int((math.factorial(N) * (N - 2)) / (math.factorial(N - 2) * 2))  # calculates the number of networks
elements = np.zeros((N_elements, 1))
costLog = np.zeros((Nsteps, N_nets))
axis_labels = np.zeros((N_nets, 3))
x_labels = ['p1_t0', 'p1_t1', 'a1_t0', 'p2_t0', 'p2_t1', 'a2_t0']
viable = np.ones((N_nets,1))

nn = []
for i in range(0, N_nets):
    nn.append(neuronets.NN(nInput, nHidden, nOut, eta1, eps1, pruning_rate, pruning_thresh))
    nn[i].initialize_weights()

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

m1_min, m1_max = rf.calibrate_motor(c, motors, 1)
rf.move2middle(m1_min, m1_max, c, motors, 1)
m2_min, m2_max = rf.calibrate_motor(c, motors, 0)
rf.move2middle(m2_min, m2_max, c, motors, 0)



# learning loop

for k in range(0, Nsteps):
    raw_a1 = np.random.randint(motor_min, high=motor_max+1)
    raw_a2 = np.random.randint(motor_min, high=motor_max+1)
    a1_t0 = rf.map2normal(raw_a1, motor_min, motor_max)
    a2_t0 = rf.map2normal(raw_a2, motor_min, motor_max)
    raw_angles = c.get_degrees_two_motors(motors)
    raw_p1_t0 = raw_angles[1]
    raw_p2_t0 = raw_angles[0]
    p1_t0 = rf.map2normal(raw_p1_t0, m1_min, m1_max)
    p2_t0 = rf.map2normal(raw_p2_t0, m2_min, m2_max)
    if raw_angles[1]-m1_min < safety_margin and raw_a1 < 0:
        raw_a1 = 0
    if m1_max - raw_angles[1]< safety_margin and raw_a1 > 0:
        raw_a1 = 0
    if raw_angles[0]-m2_min < safety_margin and raw_a2 < 0:
        raw_a2 = 0
    if m2_max - raw_angles[0]< safety_margin and raw_a2 > 0:
        raw_a2 = 0
    motors = [
        {
            'port': 1,
            'speed': raw_a2,
            'duration': 0.1
        },
        {
            'port': 8,
            'speed': raw_a1,
            'duration': 0.1
        }
    ]
    c.move_two_motors(motors)

    time.sleep(0.6)
    raw_angles = c.get_degrees_two_motors(motors)
    raw_p1_t1 = raw_angles[1]
    raw_p2_t1 = raw_angles[0]
    p1_t1 = rf.map2normal(raw_p1_t1, m1_min, m1_max)
    p2_t1 = rf.map2normal(raw_p2_t1, m2_min, m2_max)

    print('step = ', k, ' theta0 = ', p1_t0, ' a = ', a1_t0, ' theta1 = ', p1_t1)

    z = [p1_t0, p1_t1, a1_t0, p2_t0, p2_t1, a2_t0]

    l = 0
    for i in range(0, N_elements):
        for j in range(i+1, N_elements):
            for m in range(0, N_elements):
                if m != j and m != i:
                    axis_labels[l, :] = [i, j, m]
                    x1 = [z[i], z[j]]
                    d1 = z[m]
                    xa1, s11, za1, s21, y1 = nn[l].forProp(x1)
                    J = nn[l].backProp(xa1, s11, za1, s21, y1, d1)
                    costLog[k, l] = J
                    if nn[l].nHidden > 0:
                        nn[l].removeNode()
                        if nn[l].nHidden == 0:
                            viable[l] = 1
                    l += 1


print(viable)
i1 = np.linspace(-1.0, 1.0, resolution)
i2 = np.linspace(-1.0, 1.0, resolution)
outPut = np.zeros((resolution, resolution, N_nets))
X, Y = np.meshgrid(i1, i2)

for l in range(0, N_nets):
    plt.figure(l)

    plt.subplot(121)
    plt.plot(costLog[:, l])
    plt.xlabel('time(steps)')
    plt.ylabel('Cost')

    for i in range(0, resolution):
        for j in range(0, resolution):
            x1 = [i1[i], i2[j]]
            xa, s1, za, s2, y1 = nn[l].forProp(x1)
            outPut[i, j, l] = y1

    plt.subplot(122)
    b = outPut[:, :, l]
    out = np.squeeze(b)
    plt.contourf(X, Y, np.transpose(out))
    plt.xlabel(x_labels[int(axis_labels[l, 0])])
    plt.ylabel(x_labels[int(axis_labels[l, 1])])
    plt.title(x_labels[int(axis_labels[l, 2])])
    plt.colorbar()


plt.tight_layout()
plt.show()


