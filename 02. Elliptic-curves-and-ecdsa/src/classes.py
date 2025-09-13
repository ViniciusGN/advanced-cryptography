import math
import random
import src.lab1_utils as lab1_utils

IDT_ELEMENT = [0, 0]

class Group(object):
    def __init__(self, l, e, N, p, poly=None, A=None, B=None):
        self.l = l
        self.e = e
        self.N = N
        self.p = p
        self.A = A 
        self.B = B
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
        elif(self.l == "ECConZp"):
            disc = (4 * pow(self.A, 3, self.p) + 27 * pow(self.B, 2, self.p)) % self.p
            if disc != 0:
                self.e = IDT_ELEMENT[:]  # [0,0]
                return True
            return False
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
        elif(self.l == "ECConZp"):
            lambda_value = 0
            group = Group(l="ZpMultiplicative", e=1, N=self.p-1, p=self.p, A=self.A, B=self.B)

            if((g1 == IDT_ELEMENT)):
                # If g1 = idt element, return g2
                return g2
            elif((g2 == IDT_ELEMENT)):
                # If g2 = idt element, return g1
                return g1
            elif((g1[0] == g2[0]) and ((g1[1] != g2[1]) or ((g1[1] == 0)) and (g2[1] == 0))):
                # If (g1_x is equal g2_x) se if (g1_y is diff g2_y) or (g1_y and g2_y are equal 0)
                return IDT_ELEMENT
            elif((g1[0] == g2[0]) and ((g1[1] != 0) and (g2[1] != 0))):
                # If (g1_x is equal g2_x) and (g1_y and g2_y both are diff 0)
                inv = group.exp(2*g1[1] % self.p, -1)
                lambda_value = ((3*(g1[0]**2)+self.A)*inv) % self.p 
                x = (lambda_value**2 - (2*g1[0])) % self.p
                y = (lambda_value*(g1[0]-x) - g1[1]) % self.p
                return [x,y]
            elif(g1 != g2):
                inv = group.exp((g2[0] - g1[0]) % self.p, -1)
                lambda_value = ((g2[1] - g1[1])*inv) % self.p
                x = (lambda_value**2 - g1[0] - g2[0]) % self.p
                y = (lambda_value*(g1[0]-x)-g1[1]) % self.p
                return [x,y]
        
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
    def __init__(self, l, e, N, p, g, poly=None, A=None, B=None):
        Group.__init__(self, l, e, N, p, poly, A, B)
        self.g = g

    def DLbyTrialMultiplication(self, h):
        for i in range(self.N):
            if((self.exp(self.g, i) == h)):
                return i
        raise Exception("DLbyTrialMultiplication: no 'i' founded.")
    
    def testDiffieHellman(self):
        a = random.randint(1, self.N)
        b = random.randint(1, self.N)

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

    def verify(self, P):
        if(len(P) != 2):
            raise Exception("The point P must be a list with [x,y] structure.")
        x = P[0]
        y = P[1]
        left = (y * y) % self.p
        right = (x * x * x + self.A * x + self.B) % self.p

        if(P == IDT_ELEMENT):
            return True
        elif(left == right):
            return True
        else:
            return False
    
    def ecdsa_sign(self, m, sk, debug=False):
        if(debug == True):
            k = 0x7a1a7e52797fc8caaa435d2a4dace39158504bf204fbe19f14dbb427faee50ae
        else:
            # 1. Generate a secret k ∈ [1, N − 1] at random and K = kP.
            k = random.randint(1, self.N-1)

        K = self.exp(self.g, k)
        # 2. Let t be X_K mod N, the x-coordinate of K mod N
        t = K[0] % self.N
        # 3. Calculate s = (m + dt)k^−1 mod N
        group = Group(l="ZpMultiplicative", e=1, N=self.N, p=self.p, A=self.A, B=self.B)
        k_inv = pow(k, -1, self.N) % self.N # group.exp(k, -1)
        s = ((m + sk * t) * k_inv) % self.N
        # return signature = (t, s)
        return (t, s)

    def ecdsa_verif(self, m, signature, pb_key, debug=False):
        # signature = (t, s)
        t, s = signature

        if debug == True:
            # Vectors for debug (NIST)
            t1_ref = 0xb807bf3281dd13849958f444fd9aea808d074c2c48ee8382f6c47a435389a17e
            t2_ref = 0x1777f73443a4d68c23d1fc4cb5f8b7f2554578ee87f04c253df44efd181c184c
            Q1x_ref = 0x9e2c4384537e1872fb420057aac0f0afd3b44128eb8ad091a58a0adc342989f8
            Q2x_ref = 0xf825bc60b347d1b3bde9f2c8d92ca3d55cd2f5e325c7d7cc50ed0452c68d82fe

        # 1. Check that t and s are in [1, N-1].
        if (t <= 0) or (t >= self.N) or (s <= 0) or (s >= self.N):
            return False

        # 2. Compute w = s^{-1} mod N, u1 = m*w mod N, u2 = t*w mod N
        w = pow(s, -1, self.N)
        u1 = (m * w) % self.N
        u2 = (t * w) % self.N

        # Intermed points: Q1 = u1*G, Q2 = u2*Q
        Q1 = self.exp(self.g, u1)
        Q2 = self.exp(pb_key, u2)

        # R = Q1 + Q2
        R = self.law(Q1, Q2)
        if R == IDT_ELEMENT:
            return False

        # 3. The sign is valid if R.x mod N == t
        ok = ((R[0] % self.N) == t)

        if debug == True:
            print("t1 ok?   ", hex(u1) == hex(t1_ref))
            print("t2 ok?   ", hex(u2) == hex(t2_ref))
            print("Q1.x ok? ", hex(Q1[0] % self.p) == hex(Q1x_ref))
            print("Q2.x ok? ", hex(Q2[0] % self.p) == hex(Q2x_ref))
            print("ECDSA verif ->", ok)

        return ok
        
