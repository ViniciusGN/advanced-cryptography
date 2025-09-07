import classes
import random

def testLab1_part1():
    group_z23_add = classes.Group("ZpAdditive", 0, 23, 23)
    group_z23_multi = classes.Group("ZpMultiplicative", 1, 22, 23)
    print("##### First Verification:")
    print("In Z23_add : exp(5,7) = 12 ?", group_z23_add.exp(5,7) == 12)
    print("In Z23_multi : exp(5,7) = 17 ?", group_z23_multi.exp(5,7) == 17, "\n")

    print("##### Second Verification:")
    print("In Z23_add : exp(5,-1) = 18 ?", group_z23_add.exp(5,-1) == 18)
    print("In Z23_multi : exp(5,-1) = 14 ?", group_z23_multi.exp(5,-1) == 14, "\n") 

    print("##### Third Verification:")
    g = 3
    p = 809
    sgp = classes.SubGroup(l="ZpAdditive", e=0, N=p, p=p, g=g)
    i = random.randint(0, p-1) 
    h = sgp.exp(g, i)
    print(f"h value computed by exp() : {h}")
    print("DL Function value : ", sgp.DLbyTrialMultiplication(h))
    print(f"i value : {i}")

    print("##### Fourth Verification:")
    N = p - 1  # 808
    sgp_mul = classes.SubGroup(l="ZpMultiplicative", e=1, N=N, p=p, g=g)
    i2 = random.randint(0, N-1)
    h2 = sgp_mul.exp(g, i2)
    print(f"h value computed by exp() (mul) : {h2}")
    print("DL Function value (mul) : ", sgp_mul.DLbyTrialMultiplication(h2))
    print(f"i value (mul) : {i2}\n")

def testLab1_part2():
    print("##### First Verification:")
    group_z23_add = classes.SubGroup(l="ZpAdditive", e=0, N=23, p=23, g=5)
    print("testDiffieHellman: ", group_z23_add.testDiffieHellman())
    print(group_z23_add.DiffieHellman(a=5, b=6, A=2, B=7, K=12), "\n")

    print("##### Second Verification:")
    group_f256 = classes.SubGroup(l="F2^n", e=1, N=255, p=256, g=3, poly=283)
    print(group_f256.law(45,72))
    print("In F256 : 45 * 72 == 198 ?", group_f256.law(45,72) == 198)
    i = random.randint(1, 255)
    h = group_f256.exp(3, i)
    print(f"h value computed by exp() : {h}")
    print("DL Function value : ", group_f256.DLbyTrialMultiplication(h))
    print(f"i value : {i} \n")

    print("##### Third Verification:")
    print("testDiffieHellman: ", group_f256.testDiffieHellman())

    print("##### Fourth Verification:")
    i_bsgs = random.randint(1, 255)
    h_bsgs = group_f256.exp(3, i_bsgs)
    print("ComputeDL (tau=100) value : ", group_f256.ComputeDL(h_bsgs, tau=100))
    print(f"i value : {i_bsgs}")

if __name__ == "__main__":
    testLab1_part1()
    print("\n========================\n")
    testLab1_part2()
