import neuronets
import numpy as np
import matplotlib.pyplot as plt
import time
import math




np.random.seed(1)
nInput = 2
nHidden = 10
nOut = 1
eta1 = 0.01 #learning rate
eps1 = 1
pruning_rate = [0, 0.00001, 0.0001, 0.001, 0.01]
pruning_thresh = 0.1
i_mul = 10

Nsteps = 100000
resolution = 100
viable = 1
N_nets = 2
costLog = np.zeros((Nsteps, N_nets))
neuronsPruned = np.zeros((Nsteps, N_nets))

for j in range(0, 5):

    nn1 = neuronets.NN(1, 2, 3, nInput, nHidden, nOut, eta1, eps1, pruning_rate[j], pruning_thresh, viable, i_mul)
    nn1.initialize_weights()

    nn2 = neuronets.NN(4, 5, 6, nInput, nHidden, nOut, eta1, eps1, pruning_rate[j], pruning_thresh, viable, i_mul)
    nn2.initialize_weights()

    for i in range(0, Nsteps):

        x1 = [np.random.random()-0.5, np.random.random()-0.5]
        xa1, s11, za1, s21, y1 = nn1.forProp(x1)
        d1 = (np.random.random()-0.5) * 2
        J = nn1.backProp(xa1, s11, za1, s21, y1, d1)
        costLog[i, 0] = J
        nn1.removeNode()
        neuronsPruned[i, 0] = nn1.nHidden

        xa1, s11, za1, s21, y1 = nn2.forProp(x1)
        d1 = x1[0] + x1[1]
        #d1 = math.sin(x1[0]+ math.cos(x1[0]) + x1[1]*x1[1])
        J = nn2.backProp(xa1, s11, za1, s21, y1, d1)
        costLog[i, 1] = J
        nn2.removeNode()
        neuronsPruned[i, 1] = nn2.nHidden

    i1 = np.linspace(-0.5, 0.5, resolution)
    i2 = np.linspace(-0.5, 0.5, resolution)
    outPut = np.zeros((resolution, resolution, N_nets))
    X, Y = np.meshgrid(i1, i2)
    t = np.linspace(0, Nsteps, Nsteps)

    plt.figure(j)
    plt.suptitle(["pruning rate = ", pruning_rate[j]], fontsize="x-large")

    plt.subplot(241)
    plt.title('random training set')
    plt.plot(t, costLog[:, 0])
    plt.xlabel('time(steps)')
    plt.ylabel('Cost')
    plt.subplot(242)
    plt.title('random training set')
    plt.plot(t, neuronsPruned[:, 0])
    plt.xlabel('time')
    plt.ylabel('hidden neurons')
    for l in range(0, resolution):
        for m in range(0, resolution):
            x1 = [i1[l], i2[m]]
            xa, s1, za, s2, y1 = nn1.forProp(x1)
            outPut[l, m, 0] = y1

    plt.subplot(243)
    plt.title('random training set')
    Wa11_flat = nn1.Wa1.flatten()
    Wa21_flat = nn1.Wa2.flatten()
    W1_flat = np.concatenate((Wa11_flat, Wa21_flat), axis=0)
    plt.hist(W1_flat, bins='auto')
    plt.xlabel('weight size')
    plt.ylabel('number of weights')

    plt.subplot(244)
    plt.title('random training set')
    b = outPut[:, :, 0]
    out = np.squeeze(b)
    plt.contourf(X, Y, np.transpose(out))

    plt.colorbar()

    plt.subplot(245)
    plt.title('linear training set')
    plt.plot(t, costLog[:, 1])
    plt.xlabel('time(steps)')
    plt.ylabel('Cost')
    plt.subplot(246)
    plt.title('linear training set')
    plt.plot(t, neuronsPruned[:, 1])
    plt.xlabel('time')
    plt.ylabel('hiddne neurons')
    for l in range(0, resolution):
        for m in range(0, resolution):
            x1 = [i1[l], i2[m]]
            xa, s1, za, s2, y1 = nn2.forProp(x1)
            outPut[l, m, 1] = y1

    plt.subplot(247)
    plt.title('linear training set')
    Wa12_flat = nn2.Wa1.flatten()
    Wa22_flat = nn2.Wa2.flatten()
    W2_flat = np.concatenate((Wa12_flat, Wa22_flat), axis=0)
    plt.hist(W2_flat, bins='auto')
    plt.xlabel('weight size')
    plt.ylabel('number of weights')

    plt.subplot(248)
    plt.title('linear training set')
    b = outPut[:, :, 1]
    out = np.squeeze(b)
    plt.contourf(X, Y, np.transpose(out))

    plt.colorbar()

    plt.tight_layout()

    plt.figure(j+5)
    plt.title('linear training set')
    plt.plot(t, costLog[:, 1])
    plt.plot(t, neuronsPruned[:, 1]/100)
    plt.xlabel('time(steps)')
    plt.ylabel('Cost')
plt.show()
plt.savefig('books_read.png')
print('viable = ', )

