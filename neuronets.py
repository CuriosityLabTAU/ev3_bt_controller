import numpy as np
import matplotlib.pyplot as plt


class NN:

    def __init__(self, nInput, nHidden, nOutput, eta=0.1, eps=0.1):
        self.nInput = nInput
        self.nHidden = nHidden
        self.nOutput = nOutput
        self.eta = eta
        self.eps = eps

    def sig(z):
        h = np.tanh(z)
        return h

    def sigtag(z):
        stag = 1-np.multiply(NN.sig(z),NN.sig(z))
        return stag

    def initialize_weights(self):
        n = self.nInput
        p = self.nHidden
        m = self.nOutput
        eps = self.eps

        self.Wa1 = np.random.rand(p,n+1)*2*eps-eps
        self.Wa2 = np.random.rand(m,p+1)*2*eps-eps

    def forProp(self, x):
        xa = np.insert(x, 0, 1)
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
        return D1, D2

    def learn(self, x, d, itera, eta):
        bD1 = np.zeros(self.Wa1.shape)
        bD2 = np.zeros(self.Wa2.shape)
        ff = np.zeros((itera, 1))
        t = x.shape[0]

        k = 0
        for j in range(1, itera):
            J = 0
            for i in range(t):
                xa, s1, za, s2, y = NN.forProp(self, x[i, :])
                D1,D2 = NN.backProp(self, xa, s1, za, s2, y, d[i])
                bD1 += D1
                bD2 += D2
                J += NN.cost(self, d[i], y)
            k += 1
            ff[k] = J
            self.Wa2 -= eta*(bD2/t)
            self.Wa1 -= eta*(bD1/t)
            bD1 = 0
            bD2 = 0

        plt.plot(ff)
        plt.show()

    def learnNew(self, x, d, eta):
        bD1 = np.zeros(self.Wa1.shape)
        bD2 = np.zeros(self.Wa2.shape)
        t = x.shape[0]
        xa, s1, za, s2, y = NN.forProp(self, x)
        D1,D2 = NN.backProp(self, xa, s1, za, s2, y, d)
        bD1 += D1
        bD2 += D2
        J += NN.cost(self, d, y)
        self.Wa2 -= eta*(bD2/t)
        self.Wa1 -= eta*(bD1/t)



    def prepIO(self, x):
        t = x.shape[0]
        y2 = np.zeros((t, self.nOutput))
        for i in range(t):
            xa, s1, za, s2, y = NN.forProp(self, x[i, :])
            y2[i, :] = y
        return y2










