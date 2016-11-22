import neuronets
#from ev3_bt_controller import *
#import robot_fun as rf
import numpy as np
import matplotlib.pyplot as plt
import time 
import math
from robot import Robot

# neural network parameters
nInput = 2
nHidden = 10
nOut = 1

# learning parameters
eta1 = 0.1
eps1 = 1
pruning_rate = 0.0001
pruning_thresh = 0.1
i_mul = 10

# session parameters
Nsteps = 1000
resolution = 100
np.random.seed(1)

N_motors = 2  # number of motors
N_cameras = 1
N_elements = N_motors * 3 + N_cameras * 2  # each motor has three elements - p(t), p(t+1), a(t)
N = N_elements
N_nets = int((math.factorial(N) * (N - 2)) / (math.factorial(N - 2) * 2))  # calculates the number of networks
elements = np.zeros((N_elements, 1))
costLog = np.zeros((Nsteps, N_nets))
neuronsPruned = np.zeros((Nsteps, N_nets))
axis_labels = np.zeros((N_nets, 3))
x_labels = ['p1_t0', 'p1_t1', 'a1_t0', 'p2_t0', 'p2_t1', 'a2_t0', 'c1_t0', 'c1_t1']
data_log = np.zeros((Nsteps, 6))
viable_log = np.zeros((Nsteps, N_nets))

nn = []
l = 0
for i in range(0, N_elements):
    for j in range(i+1, N_elements):
        for m in range(0, N_elements):
            if m != j and m != i:
                nn.append(neuronets.NN(i, j, m, nInput, nHidden, nOut, eta1, eps1, pruning_rate, pruning_thresh, viable=1))
                nn[l].initialize_weights()
                l += 1

r1 = Robot()

# learning loop
for k in range(0, Nsteps):
    a1_t0 = (np.random.random() - 0.5) * 2
    a2_t0 = (np.random.random() - 0.5) * 2

    [p1_t0, p2_t0] = r1.read_motor_sensors()
    c1_t0 = r1.get_image()

    r1.command_motors(a1_t0, a2_t0)
    time.sleep(0.1)

    [p1_t1, p2_t1] = r1.read_motor_sensors()
    c1_t1 = r1.get_image()

    print('step = ', k, ' theta0 = ', p1_t0, ' a = ', a1_t0, ' theta1 = ', p1_t1)
    z = [p1_t0, p1_t1, a1_t0, p2_t0, p2_t1, a2_t0, c1_t0, c1_t1]
    data_log[k, :] = z

    for l in range(0, N_nets):
        x1 = [z[nn[l].input1_index], z[nn[l].input2_index]]
        d1 = z[nn[l].output1_index]
        xa1, s11, za1, s21, y1 = nn[l].forProp(x1)
        J = nn[l].backProp(xa1, s11, za1, s21, y1, d1)
        costLog[k, l] = J
        nn[l].removeNode()
        neuronsPruned[k, l] = nn[l].nHidden
        viable_log[k, l] = nn[l].viable

np.save("data_log.npy", data_log)
np.save("viable_log.npy", viable_log)

for i in range(0, N_nets):
    print(nn[i].viable)

i1 = np.linspace(-1.0, 1.0, resolution)
i2 = np.linspace(-1.0, 1.0, resolution)
outPut = np.zeros((resolution, resolution, N_nets))
X, Y = np.meshgrid(i1, i2)
t = np.linspace(0, Nsteps, Nsteps)

for l in range(0, N_nets):
    if nn[l].viable == 1:
        plt.figure(l)

        plt.subplot(221)
        plt.plot(t, costLog[:, l])
        plt.xlabel('time(steps)')
        plt.ylabel('Cost')
        plt.subplot(223)
        plt.plot(t, neuronsPruned[:, l])
        plt.xlabel('hidden neurons')
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
        plt.xlabel(x_labels[int(nn[l].input1_index)])
        plt.ylabel(x_labels[int(nn[l].input2_index)])
        plt.title(x_labels[int(nn[l].output1_index)])
        plt.colorbar()


plt.tight_layout()
plt.show()


