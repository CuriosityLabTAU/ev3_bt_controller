
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

eta1 = 0.05
eps1 = 1
pruning_rate = 0.00001
pruning_thresh = 0.1
motor_max = 30
motor_min = -30
sensor_max = 360
sensor_min = 1
Nsteps = 200
resolution = 100
safety_margin = 21

N_motors = 2
N_elements = N_motors * 3
N = N_elements
N_nets = int((math.factorial(N) * (N - 2)) / (math.factorial(N - 2) * 2))
elements = np.zeros((N_elements, 1))

nn = {}
for i in range(1, N_nets+1):
    nn[i] = neuronets.NN(nInput, nHidden, nOut, eta1, eps1, pruning_rate, pruning_thresh)
    nn[i].initialize_weights()

costLog = np.zeros((Nsteps, N_nets))

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
rf.move2middle(m1_min, m1_max, c, motors, 0)

k = 0
for x in range(0,Nsteps):
    raw_a = np.random.randint(motor_min, high=motor_max+1)
    a_t0 = rf.map2normal(raw_a, motor_min, motor_max)
    raw_angles = c.get_degrees_two_motors(motors)
    raw_theta_t0 = raw_angles[1]
    theta_t0 = rf.map2normal(raw_theta_t0, m1_min, m1_max)
    if raw_angles[1]-m1_min < safety_margin and raw_a < 0 :
        raw_a = 0
    if m1_max - raw_angles[1]< safety_margin and raw_a > 0 :
        raw_a = 0
    motors = [
        {
            'port': 1,
            'speed': 0,
            'duration': 0.1
        },
        {
            'port': 8,
            'speed': raw_a,
            'duration': 0.01
        }
    ]
    c.move_two_motors(motors)

    time.sleep(0.6)
    raw_angles = c.get_degrees_two_motors(motors)
    raw_theta_t1 = raw_angles[1]
    theta_t1 = rf.map2normal(raw_theta_t1, m1_min, m1_max)

    print('step = ', k, ' theta0 = ', theta_t0, ' a = ', a_t0, ' theta1 = ', theta_t1)

    x1 = [theta_t0, a_t0]
    d1 = theta_t1
    xa1, s11, za1, s21, y1 = nn[1].forProp(x1)
    J = nn[1].backProp(xa1, s11, za1, s21, y1, d1)
    costLog[k,1] = J
    #nn1.removeNode()

    x2 = [theta_t1, a_t0]
    d2 = theta_t0
    xa2, s12, za2, s22, y2 = nn[2].forProp(x2)
    J = nn[2].backProp(xa2, s12, za2, s22, y2, d2)
    costLog[k,2] = J
    #nn2.removeNode()

    x3 = [theta_t1, theta_t0]
    d3 = a_t0
    xa3, s13, za3, s23, y3 = nn[3].forProp(x3)
    J = nn[3].backProp(xa3, s13, za3, s23, y3, d3)
    costLog[k,3] = J
    #nn3.removeNode()

    k += 1

xa, s1, za, s2, y1 = nn[3].forProp([1,-1])
print('y1 = ', y1)

plt.figure(1)
plt.subplot(321)
plt.plot(costLog[:,1])
plt.xlabel('time(steps)')
plt.ylabel('Cost')

plt.subplot(323)
plt.plot(costLog[:,2])
plt.xlabel('time(steps)')
plt.ylabel('Cost')

plt.subplot(325)
plt.plot(costLog[:,3])
plt.xlabel('time(steps)')
plt.ylabel('Cost')

i1 = np.linspace(-1.0, 1.0, resolution)
i2 = np.linspace(-1.0, 1.0, resolution)
o1 = np.zeros((resolution, resolution))
o2 = np.zeros((resolution, resolution))
o3 = np.zeros((resolution, resolution))

for i in range(0, resolution):
    for j in range(0, resolution):
        x1 = [i1[i], i2[j]]
        xa, s1, za, s2, y1 = nn[1].forProp(x1)
        xa, s1, za, s2, y2 = nn[2].forProp(x1)
        xa, s1, za, s2, y3 = nn[3].forProp(x1)
        print('x = ', x1[0], ' y = ', x1[1], 'y3 = ', y3)
        o1[i, j] = y1
        o2[i, j] = y2
        o3[i, j] = y3

X, Y = np.meshgrid(i1, i2)

plt.subplot(322)
plt.contourf(X, Y, np.transpose(o1))
plt.xlabel('p(t-1)')
plt.ylabel('m(t)')
plt.title('V(p(t)|p(t-1),m(t)')
plt.colorbar()

plt.subplot(324)
plt.contourf(X, Y, np.transpose(o2))
plt.xlabel('p(t)')
plt.ylabel('m(t)')
plt.title('V(p(t-1)|p(t),m(t)')
plt.colorbar()

plt.subplot(326)
plt.contourf(X, Y, np.transpose(o3))
plt.xlabel('p(t)')
plt.ylabel('p(t-1)')
plt.title('V(m(t)|p(t),p(t-1)')
plt.colorbar()

plt.tight_layout()
plt.show()


