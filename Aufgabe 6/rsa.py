#!/bin/python3

import argparse
import math
import os
import random as rand


def main():
    private_key = 11
    public_key = 429522609848932931
    n = 4724748713148721723
    n_bits = int(((math.log2(n))+1)/8) + 1

    # Aktueller Pfad der Python Datei
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Klartext einlesen
    file = open(dir_path + "/clear.txt", "r")
    text = file.read()
    file.close()

    # Text in Bits umwandeln und Blöcke trennen
    blocks = get_blocks(text, 4)
    print(blocks[:10])

    # Verschlüsseln
    encrypted = encrypt(blocks, public_key, n_bits, n)
    file = open(dir_path + "/encrypted.txt", "wb")
    file.write(b''.join(encrypted))
    file.close()
    print(encrypted[:10])

    # Entschlüsseln

    decrypted = decrypt(encrypted, private_key, 4, n)
    file = open(dir_path + "/decrypted.txt", "wb")
    file.write(b''.join(decrypted))
    file.close()
    print(decrypted[:10])

    pass


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


def decrypt(blocks: [b''], private_key: int, length: int, n: int):
    return [(power(int.from_bytes(block, 'big'), private_key, n)).to_bytes(length, 'big') for block in blocks]
    pass


def encrypt(blocks: [b''], public_key: int, length: int, n: int):
    return [(power(int.from_bytes(block, 'big'), public_key, n)).to_bytes(length, 'big') for block in blocks]
    pass


def get_text(blocks: [b'']):
    pass


def get_blocks(text: str, byte_length: int):
    text_bytes = text.encode()
    counter = 1
    block = b''
    blocks = []
    for char in text_bytes:
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


if __name__ == "__main__":
    main()
