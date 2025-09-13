#!/usr/bin/python3

from math import log

def deg(P):
    # Retourne le degré de P où P est un polynome (élément d'un corps de F_2^n)
    # représenté par un entier entre 0 et 2^n - 1
    if P == 0:
        return -1
    if P == 1:
        return 0
    if P > 1:
        return int(log(P, 2)) 
    else:
        print("erreur dans la fonction deg : P < 0") 
        return 0 

def affiche(x):
    s = ""
    if x & 1: s += "1" 
    if (x >> 1) & 1:
       if s != "" : s += "+\u03B1"
       else : s += "\u03B1"
    k = int(log(x, 2)) + 1
    for i in range(2, k + 1):
         if (x >> i) & 1 : 
             if s != "" : s += "+\u03B1^%s"%i
             else :  s += "\u03B1^%s"%i
    return s

def testAffiche():    
    print("affiche(45)=",affiche(45))
    print("affiche(72)=",affiche(72))
    print("affiche(198)=",affiche(198))
    
if __name__ == "__main__":         
    testAffiche()
