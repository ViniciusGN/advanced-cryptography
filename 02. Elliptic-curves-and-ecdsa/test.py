import src.classes as classes
import random
from hashlib import sha256

def testLab2_part1():
    A_p256 = -3
    B_p256 = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
    N_p256 = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
    Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
    Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
    G_p256 = [Gx, Gy]
    p_p256 = (2**256) - (2**224) + (2**192) + (2**96) - 1
    ec_p256 = classes.SubGroup(l="ECConZp", e=0, N=N_p256, p=p_p256, g=G_p256, A=A_p256, B=B_p256)

    GooglePublicKey = open("./docs/google.der", 'rb')
    PK = GooglePublicKey.read()
    Pkx = int.from_bytes(PK[0xbf:0xdf], byteorder='big')
    Pky = int.from_bytes(PK[0xdf:0xff], byteorder='big')
    GooglePublicKey.close()
    print(f'Pkx = {hex(Pkx)} \nPky = {hex(Pky)}')

    print(f'P_Google Certificates is in the P256 EC ? {ec_p256.verify(P=[Pkx, Pky])}')

    print(f'Testing DH in EC: {ec_p256.testDiffieHellman()}')
          
def testLab2_part2():
    A_p256 = -3
    B_p256 = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
    N_p256 = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
    Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
    Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
    G_p256 = [Gx, Gy]
    p_p256 = (2**256) - (2**224) + (2**192) + (2**96) - 1
    ec_p256 = classes.SubGroup(l="ECConZp", e=0, N=N_p256, p=p_p256, g=G_p256, A=A_p256, B=B_p256)

    sk = 0xc477f9f65c22cce20657faa5b2d1d8122336f851a508a1ed04e479c34985bf96
    t = 0x2b42f576d07f4165ff65d1f3b1500f81e44c316f1f0b3ef57325b69aca46104f
    s = 0xdc42c2122d6392cd3e3a993a89502a8198c1886fe69d262c4b329bdb6b63faf1

    m = "Example of ECDSA with P-256"
    print("message m is: ", m)
    h = int(sha256(m.encode('utf-8')).hexdigest(), 16)
    print("Hash of m is: ", h)

    # Test sign (k via debug=True)
    sign = ec_p256.ecdsa_sign(h, sk, debug=True)
    print("t is correct? ", (hex(sign[0]) == hex(t)))
    print("s is correct? ", (hex(sign[1]) == hex(s)))

    # Generate the public key Q = sk * G and check if it is in the curve
    Q = ec_p256.exp(G_p256, sk)
    print("Public key Q is on curve? ", ec_p256.verify(Q))

    # Verify the signature (debug=True prints t1, t2, Q1.x, Q2.x)
    ok = ec_p256.ecdsa_verif(h, sign, Q, debug=True)
    print("ECDSA verify OK? ", ok)

if __name__ == "__main__":
    print("========================")
    print("Lab02 - Elipitic Curves\n")
    testLab2_part1()
    print("\n========================\n")
    testLab2_part2()
    
# Optional: sign external files with Alice's key and verify with OpenSSL. Output of commands below.  

# PS C:\Users\User\Desktop\TP_CryptoAvance_MOREIRA_Vinicius_Lab2\docs> openssl dgst -sha256 -sign ecdhkeyAlice.der -out Lab2.sig Lab2.pdf
# PS C:\Users\User\Desktop\TP_CryptoAvance_MOREIRA_Vinicius_Lab2\docs> openssl ec -inform DER -in ecdhkeyAlice.der -pubout -out AlicePub.pem
# read EC key
# writing EC key
# PS C:\Users\User\Desktop\TP_CryptoAvance_MOREIRA_Vinicius_Lab2\docs> openssl dgst -sha256 -verify AlicePub.pem -signature Lab2.sig Lab2.pdf
# Verified OK