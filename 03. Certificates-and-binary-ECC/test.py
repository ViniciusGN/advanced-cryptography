import src.classes as classes
import random
from hashlib import sha384, sha1

def testLab3_part1():
    # Recover P-384 parameters from FIPS 186-4, appendix D
    A_384 = -3
    B_384 = 0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef
    N_384 = 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643
    Gx = 0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7
    Gy = 0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f
    G_384 = [Gx, Gy]
    p_384 = 39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319
    ec_384 = classes.SubGroup(l="ECConZp", e=0, N=N_384, p=p_384, g=G_384, A=A_384, B=B_384)

    # Open the CA DER file to get the Pub_Key to verify the signature (is this institution that signed the file)
    E6CAcert = open("./docs/E6.der", 'rb')
    PK = E6CAcert.read()
    Pkx = int.from_bytes(PK[0xe0+12:0xe0+12+48], byteorder='big')
    Pky = int.from_bytes(PK[0xe0+12+48:0xe0+12+48+48], byteorder='big')

    e6_pk = [Pkx,Pky]   # Pub_Key is Px and Py recovered in the file
    print(f'P_E6 Certificates is in the P384 EC ? {ec_384.verify(P=[Pkx, Pky])}') # Verify if this is correct (exist in EC)
    print(f'Pkx = {hex(Pkx)} \nPky = {hex(Pky)}')
    E6CAcert.close()

    # Then open Wikipedia DER file to get the first part and hash them, and the signature part too
    WikiDERfile = open("./docs/wikipedia.der", 'rb')
    cert = WikiDERfile.read()
    cert_without_sig = cert[4:4+1513]
    WikiDERfile.close() 

    hash_value = sha384(cert_without_sig).digest() # Hash the first part and verify if is correct 
    print("Hash of the certificate is: ", hash_value)

    # s starts in 0x600, with 48 bytes
    s_start = 0x600
    s_value_wiki = cert[s_start:s_start + 48]
    print("S value of the certificate is: ", s_value_wiki.hex())

    # t starts in 0x630, with 49 bytes (and starts with 1 byte zero)
    t_start = s_start + 50
    t_value_wiki = cert[t_start:t_start + 49]
    print("T value of the certificate is: ", t_value_wiki.hex())

    # Transform everything in integer to perform the calculus
    s_int = int.from_bytes(t_value_wiki, byteorder='big')
    t_int = int.from_bytes(s_value_wiki, byteorder='big')
    hash_value_int = int.from_bytes(hash_value, byteorder='big')
    signature = [t_int, s_int] # The signature is t and s [IMPORTANT: For some reason, I inverted them in array position]

    # Test sign (debug=True is for the Lab2 exercice, dont use here)
    ok = ec_384.ecdsa_verif(m=hash_value_int, signature=signature, pb_key=e6_pk, debug=False)
    print("ECDSA verify OK? ", ok)

def testLab3_part2():
    # Recover B-163 parameters from FIPS 186-4, appendix D
    A_b163 = 1
    B_b163 = 2982236234343851336267446656627785008148015875581
    N_b163 = 0x40000000000000000000292FE77E70C12A4234C33
    Gx = 5759917430716753942228907521556834309477856722486
    Gy = 1216722771297916786238928618659324865903148082417
    G_b163 = [Gx, Gy]
    # irreducible polynomial x^163 + x^7 + x^6 + x^3 + 1
    poly = (1 << 163) | (1 << 7) | (1 << 6) | (1 << 3) | 1
    ec_b163 = classes.SubGroup(l="ECC_F2^n", e=0, N=N_b163, p=163, g=G_b163, poly=poly ,A=A_b163, B=B_b163)

    # Prepare the message and compute its SHA-1 hash
    m = "Example of ECDSA with B-163"
    h_hex = sha1(m.encode("utf-8")).hexdigest()
    h_int = int(h_hex, 16)
    print("message m is: ", m)
    print("Hash of m is: ", h_hex)

    # Group law tests
    print("\n##### First Verification: ")
    # Test Diffie-Hellman key exchange on B-163
    print("testDiffieHellman: ", ec_b163.testDiffieHellman())
    # Verify that the base point G lies on the curve
    print("Verify(G): ", ec_b163.verify(G_b163))

    # ECDSA sign/verify test
    sk = random.randint(1, N_b163 - 1)  # Generate a random private key
    Q  = ec_b163.exp(ec_b163.g, sk) # Compute the corresponding public key
    sig = ec_b163.ecdsa_sign(h_int, sk)     # Sign the message hash with sk
    ok  = ec_b163.ecdsa_verif(h_int, sig, Q)    # Verify the signature with Q

    # Key generation and curve membership
    print("\n##### Second Verification: ")
    print("ECDSA signature: ", sig)     # Generate another private key
    print("ECDSA verify: ", ok)        # Verify the signature with Q
    
    sk = random.randint(1, N_b163 - 1)
    Q = ec_b163.exp(G_b163, sk)

    print("\n##### Third Verification: ")
    print("Private key (d):", sk)
    print("Public key (Q):", Q)
    # Verify that the public key Q lies on B-163
    print("Verify(Q):", ec_b163.verify(Q))
    # Verify that Q = d*G
    print("Check exp(G,sk) == Q ?", Q == ec_b163.exp(ec_b163.g, sk))
    
def testLab3_part3():
    print("Not implemented...")
    
def testLab3_attacks():
    print("Not implemented...")

if __name__ == "__main__":
    print("========================")
    print("Lab03 - Elliptic Curves Cryptography\n")
    testLab3_part1()
    print("\n========================\n")
    testLab3_part2()