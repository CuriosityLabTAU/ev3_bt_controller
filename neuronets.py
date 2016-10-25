import numpy as np
import matplotlib.pyplot as plt


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

            weight_sum1 = np.sum(abs_Wa1, axis=1)
            weight_sum2 = np.sum(abs_Wa2, axis=0)
            weight_sum2 = weight_sum2[1:]

            total_sum = weight_sum1 + weight_sum2

            print('total sum = ', total_sum)

            prune_index = 1000

            for i in range(0, self.nHidden):
                if total_sum[i] < self.pruning_thresh:
                    prune_index = i
                    self.nHidden -= 1
                    break

            if prune_index < 999:
                self.Wa1 = np.delete(self.Wa1, prune_index, 0)
                self.Wa2 = np.delete(self.Wa2, prune_index + 1, 1)

            if self.nHidden == 0:
                self.viable = 0
            if self.nHidden == 2 and total_sum[0]>total_sum[1]*self.i_mul:
                self.viable = 0
            if self.nHidden == 2 and self.i_mul*total_sum[0]<total_sum[1]:
                self.viable = 0


















