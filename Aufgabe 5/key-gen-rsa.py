#!/bin/python3

import argparse
import math
import os
import random as rand


def main():
    print("Genutzte Primzahlen")
    p, q = get_prims(2048, 2048*2)
    print("p: %s" % p)
    print("q: %s" % q)
    phi = ((p-1)*(q-1))

    public_key = 3

    while(ggt(public_key, phi) != 1):
        public_key += 1

    print("Public Key: %s" % public_key)

    private_key = (inverse(public_key, (p-1)*(q-1)) % phi)
    print("Private Key: %s" % private_key)
    print((public_key * private_key) % phi)
    #print(inverse(693, 147))
    pass


def miller_rabin(n):
    zahlen = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    # Primzahl
    if n == 2:
        return True

    # Gerade zahlen sind keine Primzahlen
    if n % 2 == 0:
        return False

    # m und k ausrechnen
    k, m = 0, n - 1
    while m % 2 == 0:
        k += 1
        m //= 2

    # Miller Rabin für die oben stehenden Zahlen
    for a in zahlen:
        if(a < n):
            x = pow(a, m, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(k - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
    return True


def get_prims(a: int, b: int):
    """
    Range in Bit
    a -> max

    b -> min
    """
    p = rand.randint(2**a, 2**b - 1)
    while(miller_rabin(p) == False):
        p += 1

    q = rand.randint(2**a, 2**b - 1)
    while(miller_rabin(q) == False):
        q += 1

    return (p, q)


def ggt(a, b):
    """
    Kleinsten gemeinsamen Teiler von a und b
    a -> Zahl

    b -> Zahl
    """
    a, b, d = euclid_step(a, b)
    d = 1
    while b != 0:
        a, b, d = euclid_step(a, b)
    return a


def euclid_step(a, b):
    """
    Ein Schritt des euklidischen Algorithmus
    a -> Zahl

    b -> Tahl
    """
    d = a // b
    r = abs(a - (b * d))
    # print("%s = %s * %s + %s" % (a, d, b, r))
    return (b, r, d)
    pass


def inverse(a: int, b: int):
    """
    a -> Zahl desen inverses zu finden ist

    b -> Basis
    """
    a1 = a
    b1 = b

    # Definieren der ersten p unq q Zahlen
    p = [1, 0]
    q = [0, 1]
    d = 1

    # Erste Euclid-Runde ohne Erweitert
    a, b, d = euclid_step(a, b)

    while b != 0:
        # Formel aus der Vorlesung für erweiterten euklidischen Algorithmus
        p.append(p[len(p)-2] - d * p[len(p)-1])
        q.append(q[len(q)-2] - d * q[len(q)-1])
        a, b, d = euclid_step(a, b)

    return p.pop()


if __name__ == "__main__":
    main()
