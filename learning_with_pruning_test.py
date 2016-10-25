import neuronets
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
pruning_rate = 0.002
pruning_thresh = 0.1
i_mul = 10
Nsteps = 461
resolution = 100
viable = 1
N_nets = 2
costLog = np.zeros((Nsteps, N_nets))
neuronsPruned = np.zeros((Nsteps, N_nets))

nn1 = neuronets.NN(1, 2, 3, nInput, nHidden, nOut, eta1, eps1, pruning_rate, pruning_thresh, viable))
nn1.initialize_weights()

nn2 = neuronets.NN(1, 2, 3, nInput, nHidden, nOut, eta1, eps1, pruning_rate, pruning_thresh, viable))
nn2.initialize_weights()

