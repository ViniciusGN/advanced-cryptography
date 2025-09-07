import math
import random
import lab1_utils

class Group(object):
    def __init__(self, l, e, N, p, poly=None):
        self.l = l
        self.e = e
        self.N = N
        self.p = p
        self.poly = poly
        if self.checkParameters() != True:
            raise Exception("Problem with parameters")
    
    def checkParameters(self):
        if(self.l == "ZpAdditive"):
            if(self.e == 0):
                return True
            else:
                return False
        elif(self.l == "ZpMultiplicative"):
            if(self.e == 1):
                return True
            else:
                return False
        elif(self.l == "F2^n"):
            if self.poly is None:
                return False
            if self.e != 1: # identity 'e' must be 1 for multiplicative F2^n
                return False
            n = lab1_utils.deg(self.poly) # 'poly' must have degree >= 1
            if n <= 0:
                return False
            return True
        else:
            raise Exception("Problem with parameters: l is unknown")

    def law(self, g1, g2):
        if(self.l == "ZpAdditive"):
            return ((g1 + g2) % self.p)
        elif(self.l == "ZpMultiplicative"):
            return ((g1 * g2) % self.p)
        elif(self.l == "F2^n"):
            # (1)
            result_p = 0
            # (2)
            while(g2 != 0):
                if((g2 & 1) > 0): # (2a)
                    result_p = result_p ^ g1
                g1 = g1 << 1 # (2b)
                if((g1 & (1 << lab1_utils.deg(self.poly))) > 0):
                        g1 = g1 ^ self.poly # (2c)
                g2 = g2 >> 1 # (2d)
            # (3)
            return result_p
        
    def exp(self, g, k):
        k %= self.N # Ensure k is in the correct range
        if(k == 0):
            return self.e
        elif(k == -1): 
            return self.exp(g, self.N - 1)
        else:
            h0 = self.e
            h1 = g
            # Binary representation of k: t <- log2(k)
            # bin() function return us '0b...', so we must take the data after 2nd value
            t = list(map(int, bin(k)[2:]))

            # Since t saves the binary value from most signf to the least, we can use the for loop as:
            for i in range(len(t)):
                if(t[i] == 0):
                    h1 = self.law(h0, h1)
                    h0 = self.law(h0, h0)
                else:
                    h0 = self.law(h0, h1)
                    h1 = self.law(h1, h1)
            return h0
        
class SubGroup(Group):
    def __init__(self, l, e, N, p, g, poly=None):
        Group.__init__(self, l, e, N, p, poly)
        self.g = g

    def DLbyTrialMultiplication(self, h):
        for i in range(self.N):
            if((self.exp(self.g, i) == h)):
                return i
        raise Exception("DLbyTrialMultiplication: no 'i' founded.")
    
    def testDiffieHellman(self):
        a = random.randint(0, self.N)
        b = random.randint(0, self.N)

        A = self.exp(self.g, a)
        B = self.exp(self.g, b)

        if(self.exp(A, b) == self.exp(B, a)):
            return True
        else:
            return False
    
    def DiffieHellman(self, a, b, A, B, K):
        if((self.exp(self.g, a) == A) and
           (self.exp(self.g, b) == B) and
           (self.exp(A, b) ==  self.exp(B, a)) and
           (self.exp(A, b) == K)
           ):
            return True
        else:
            return False
        
    def DLbyBabyStepGiantStep(self, h):
        # 1. 
        w0 = math.isqrt(self.N)
        w = w0 if w0 * w0 == self.N else (w0 + 1)

        # 2.
        gw = self.exp(self.g, w)   # g^w
        T = {}
        val = self.e               # val = g^(0*w) = e
        for i in range(w + 1):     # 0..w
            if val not in T:
                T[val] = i
            val = self.law(val, gw)  # val <- val * g^w

        # 3.
        for j in range(w + 1):
            # 3.1 x ← h * g^(-j)
            minus_j = self.exp(self.g, -j)
            x = self.law(h, minus_j)
            # 3.2 
            if x in T:
                i = T[x]
                return (w * i + j) % self.N
        raise Exception("DLbyBabyStepGiantStep: no solution found (unexpected for cyclic subgroup).")

    def ComputeDL(self, h, tau=1000):
        if self.N <= tau:
            return self.DLbyTrialMultiplication(h)
        else:
            return self.DLbyBabyStepGiantStep(h)