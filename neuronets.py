import numpy as np
import matplotlib.pyplot as plt


class NN:

    def __init__(self, nInput, nHidden, nOutput, eta=0.1, eps=0.1, pruning=0.001):
        self.nInput = nInput
        self.nHidden = nHidden
        self.nOutput = nOutput
        self.eta = eta
        self.eps = eps
        self.pruning = pruning

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
        print(self.Wa1.shape)
        print(xa.shape)
        s1 = np.dot(self.Wa1, xa)
        z = NN.sig(s1)
        za = np.insert(z, 0, -1)
        s2 = np.dot(self.Wa2, za)
        y = s2 #NN.sig(s2)
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
        self.Wa2 -= self.eta * D2 + self.pruning * np.sign(self.Wa2)
        self.Wa1 -= self.eta * D1 + self.pruning * np.sign(self.Wa1)
        return self.cost(d, y)

    def removeNode(self):
        pass









