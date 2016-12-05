import numpy as np
import matplotlib.pyplot as plt
from random import shuffle


class NN:

    def __init__(self, input1_index, input2_index, output1_index, nInput, nHidden, nOutput, eta=0.1, eps=0.1, pruning_rate=0.0001, pruning_thresh=1000, viable=1, i_mul=10):
        self.nInput = nInput
        self.nHidden = nHidden
        self.nOutput = nOutput
        self.eta = eta
        self.eps = eps
        self.pruning_rate = pruning_rate
        self.pruning_thresh = pruning_thresh
        self.input1_index = input1_index
        self.input2_index = input2_index
        self.output1_index = output1_index
        self.viable = viable
        self.i_mul = i_mul

        self.z_memory = []
        self.memory_size = 10
        self.memory_index = 0

        self.image_patch = 1

    def sig(z):
        h = np.tanh(z)
        return h

    def sigtag(z):
        stag = 1-np.multiply(NN.sig(z),NN.sig(z))
        return stag

    def initialize_weights(self, eps_in=None):
        n = self.nInput
        p = self.nHidden
        m = self.nOutput
        if eps_in is not None:
            eps = eps_in
        else:
            eps = self.eps
        self.Wa1 = np.random.rand(p,n+1)*2*eps-eps
        self.Wa2 = np.random.rand(m,p+1)*2*eps-eps

    def forProp(self, x):
        xa = np.insert(x, 0, 1)
        #print(self.Wa1.shape)
        #print(xa.shape)
        s1 = np.dot(self.Wa1, xa)
        z = NN.sig(s1)
        za = np.insert(z, 0, -1)
        s2 = np.dot(self.Wa2, za)
        y = NN.sig(s2)
        return xa, s1, za, s2, y

    def cost(self, d, y):
        e = d-y
        J = (1/2)*np.dot(e, e)
        return J

    def backProp(self, xa, s1, za, s2, y, d):
        e2 = d-y
        sigtag2 = NN.sigtag(s2)
        d2 = np.multiply(e2, sigtag2)
        D2 = np.outer(-d2, za.T)
        sigtag1 = NN.sigtag(s1)
        p = self.Wa2.shape[1]-1
        W2 = self.Wa2[:, 1:p+1]
        e1 = np.dot(W2.T, d2)
        d1 = e1*sigtag1
        D1 = np.outer(-d1, xa.T)
        self.Wa2 -= self.eta * D2 + self.pruning_rate * np.sign(self.Wa2)
        self.Wa1 -= self.eta * D1 + self.pruning_rate * np.sign(self.Wa1)
        return self.cost(d, y)


    def removeNode(self):

        if self.nHidden > 0:
            abs_Wa1 = np.absolute(self.Wa1)
            abs_Wa2 = np.absolute(self.Wa2)
            Nw = abs_Wa1.shape
            #print('shape Wa1 = ' , Nw)

            weight_sum1 = np.sum(abs_Wa1, axis=1)
            weight_sum2 = np.sum(abs_Wa2, axis=0)
            weight_sum2 = weight_sum2[1:]

            total_sum = weight_sum1 + weight_sum2

            input_weight_sum = np.sum(abs_Wa1, axis=0)

            if input_weight_sum[2]>input_weight_sum[1]*self.i_mul:
                self.viable = 0
            if input_weight_sum[1]>input_weight_sum[2]*self.i_mul:
                self.viable = 0
                #self.Wa1 = np.zeros(self.Wa1.shape)
                #self.Wa2 = np.zeros(self.Wa2.shape)
                #print('Wa1 = ', self.Wa1)

            prune_index = 1000

            for i in range(0, self.nHidden):
                if total_sum[i] < self.pruning_thresh:
                    prune_index = i
                    self.nHidden -= 1
                    if self.nHidden == 0:
                        self.viable = 0
                    break

            if prune_index < 999:
                self.Wa1 = np.delete(self.Wa1, prune_index, 0)
                self.Wa2 = np.delete(self.Wa2, prune_index + 1, 1)


    def organize_training_set(self, z_memory):
        # receives z_memory
        training_set = []
        for m in range(0, len(z_memory)):
            for p in range(0, z_memory[m][-1].flatten().shape[0]):      # only for first level (higher, are patches)
                t_set = z_memory[m][0:-2]                    # all the non-image states
                t_set.append(z_memory[m][-2].flatten()[p])   # the pixel p from the last-minus-one image
                t_set.append(z_memory[m][-1].flatten()[p])   # the pixel p from the last image
                training_set.append(t_set)
        shuffle(training_set)
        return training_set

    def learn(self, z):
        self.z_memory[self.memory_index % self.memory_size] = z         # update memory buffer
        self.memory_index += 1

        training_set = self.organize_training_set(self.z_memory)        # generate training_set from memory

        for t in training_set:                                          # go over all training set

            x11 = np.asarray(t[self.input1_index])
            x12 = np.asarray(t[self.input2_index])
            d11 = np.asarray(t[self.output1_index])

            x11 = x11.flatten()
            x12 = x12.flatten()
            d11 = d11.flatten()
            size_x11 = x11.shape[0]
            size_x12 = x12.shape[0]
            size_d11 = d11.shape[0]
            N_batch = np.amax([size_x11, size_x12, size_d11])
            if size_x11 == 1:
                x11 = np.concatenate(np.ones((N_batch, 1)) * x11[0], axis=0)
            if size_x12 == 1:
                x12 = np.concatenate(np.ones((N_batch, 1)) * x12[0], axis=0)
            if size_d11 == 1:
                #d11 = np.ones((N_batch, 1)) * d11[0]
                d11 = np.concatenate(np.ones((N_batch, 1)) * d11[0], axis=0)
            eta_batch = self.eta/N_batch
            D1 = 0
            D2 = 0
            for i in range(0, N_batch):
                x1 = [x11[i], x12[i]]
                d12 = d11[i]
                xa, s1, za, s2, y1 = self.forProp(x1)
                e2 = d12-y1
                sigtag2 = NN.sigtag(s2)
                d2 = np.multiply(e2, sigtag2)
                D2 += np.outer(-d2, za.T)
                sigtag1 = NN.sigtag(s1)
                p = self.Wa2.shape[1]-1
                W2 = self.Wa2[:, 1:p+1]
                e1 = np.dot(W2.T, d2)
                d1 = e1*sigtag1
                D1 += np.outer(-d1, xa.T)
            self.Wa2 -= eta_batch * D2 + self.pruning_rate * np.sign(self.Wa2)
            self.Wa1 -= eta_batch * D1 + self.pruning_rate * np.sign(self.Wa1)
            J = self.cost(d12, y1)
            self.removeNode()
        return J


















