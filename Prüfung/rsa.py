#!/bin/python3

import argparse
import math
import os
import random as rand


def power(b: int, p: int, n: int):
    """
    Berechnet b^p (mod n)
    Komplexität O(log p)
    b -> int
    p -> int
    res -> int
    """
    res = 1
    while p:
        # Nur multiplizieren wenn Bit 1 ist
        if p & 0x1:
            res = (res * b) % n
        b = (b**2) % n
        p >>= 1
    return res


def decrypt(private_key: int, n: int, inputfile, output):
    # Kryptotext einlesen
    file = open(inputfile, "rb")
    text = file.read()
    file.close()

    # Text in Bits umwandeln und Blöcke trennen
    blocks = get_blocks(text, int(((math.log2(n))+1)/8) + 1)

    length = 4

    dencrypted = [(power(int.from_bytes(block, 'big'), private_key, n)).to_bytes(
        length, 'big') for block in blocks]
    file = open(output, "wb")
    file.write(b''.join(dencrypted))
    file.close()
    pass


def encrypt(public_key: int, n: int, inputfile, output):
    # Klartext einlesen
    file = open(inputfile, "rb")
    text = file.read()
    file.close()

    # Text in Bits umwandeln und Blöcke trennen
    blocks = get_blocks(text, 4)

    length = int(((math.log2(n))+1)/8) + 1

    encrypted = [(power(int.from_bytes(block, 'big'), public_key, n)
                  ).to_bytes(length, 'big') for block in blocks]

    file = open(output, "wb")
    file.write(b''.join(encrypted))
    file.close()
    pass


def get_text(blocks: [b'']):
    pass


def get_blocks(text: str, byte_length: int):
    counter = 1
    block = b''
    blocks = []
    for char in text:
        block = block + char.to_bytes(1, 'big')
        if(counter == byte_length):
            blocks.append(block)
            block = b''
            counter = 1
            pass
        else:
            counter += 1
        pass

    if(counter != 0):
        while(counter != byte_length + 1):
            block = block + b'\x00'
            counter += 1
            pass
        blocks.append(block)
        pass

    return blocks


def make_key(path):
    print("Genutzte Primzahlen")
    p, q = get_prims(32, 64)
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

    file = open(path, "w")
    file.write("Public Key: %s\nPrivate Key: %s\nn: %s" %
               (public_key, private_key, p*q))
    file.close()
    return((public_key, private_key, p*q))
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
    Input
    a -> min Bit
    b -> max Bit

    Rückgabe
    p -> int
    q -> int

    Wobei a < p*q < b 
    """
    p = 0
    q = 0
    while True:
        p = rand.randint(1, 2**a - 1)
        q = rand.randint(1, int((2**b - 1)/p))

        while(miller_rabin(p) == False):
            p += 1
        while(miller_rabin(q) == False):
            q += 1

        if(p*q > 2**a - 1 and p*q < 2**b - 1):
            break

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
