#!/bin/python3

import argparse
import math
import os
import random as rand


def enrcypt(key, output, input):
    file = open(input, "rb")
    input_blocks = getblocks(file.read(), 128)
    round_keys = makeroundkeys(key=int(key, 16))

    new_blocks = []

    # Verschlüsseln der blöcke
    for block in input_blocks:
        new_blocks.append(encrypt_block(block, round_keys))
        pass

    # Schreiben des Ergebniss
    file = open(output, "wb")
    file.write(b''.join(new_blocks))
    file.close()
    print("Datei wurde erfolgreich verschlüßelt.")
    print("Schlüssel: %s" % key)
    return round_keys
    pass


def decrypt(key, output, input):
    file = open(input, "rb")
    input_blocks = getblocks(file.read(), 128)
    round_keys = makeroundkeys(key=int(key, 16))

    # Rheienfolge der Schlüssel umdrehen
    round_keys = round_keys[::-1]

    new_blocks = []

    # Verschlüsseln (nur umgekehrt)
    for block in input_blocks:
        new_blocks.append(encrypt_block(block, round_keys))
        pass

    # Schreiben des Ergebniss
    file = open(output, "wb")
    file.write(b''.join(new_blocks))
    file.close()
    print("Datei wurde erfolgreich entschlüßelt.")
    print("Schlüssel: %s" % key)
    pass


permutation_list = [39, 46, 57, 29, 50, 36, 14, 8, 45, 31, 53, 21, 56, 55, 32, 30, 16, 38, 47, 37, 7, 5, 27, 49, 48, 58, 26, 42, 60,
                    23, 12, 44, 24, 17, 6, 54, 2, 34, 62, 35, 22, 15, 4, 43, 40, 11, 51, 52, 1, 33, 28, 61, 18, 13, 59, 19, 0, 41, 20, 10, 3, 9, 25, 63]

s_box = [229, 25, 220, 149, 5, 69, 246, 195, 210, 19, 89, 116, 170, 147, 166, 30, 28, 254, 15, 59, 247, 81, 73, 231, 248, 235, 6, 105, 151, 102, 179, 150, 228, 126, 171, 22, 61, 128, 79, 215, 1, 0, 24, 100, 17, 183, 67, 35, 68, 31, 146, 239, 38, 184, 107, 23, 65, 63, 51, 27, 255, 122, 165, 37, 226, 57, 221, 84, 187, 76, 207, 173, 16, 142, 111, 244, 87, 188, 118, 211, 224, 214, 137, 141, 222, 192, 3, 113, 201, 88, 234, 33, 139, 191, 36, 40, 29, 135, 249, 20, 237, 34, 124, 14, 186, 43, 108, 26, 197, 198, 103, 98, 180, 45, 39, 253, 110, 185, 4, 7, 54, 205, 52, 64, 223, 162, 189, 219, 75,
         172, 18, 93, 50, 194, 119, 160, 145, 250, 117, 153, 161, 114, 206, 13, 83, 58, 94, 148, 32, 121, 251, 240, 53, 217, 101, 144, 130, 177, 243, 10, 196, 245, 12, 125, 134, 138, 133, 127, 155, 181, 74, 158, 60, 190, 174, 123, 242, 42, 202, 136, 44, 225, 8, 55, 159, 167, 70, 62, 109, 66, 86, 227, 157, 168, 71, 106, 178, 104, 212, 99, 82, 143, 238, 80, 140, 152, 85, 47, 203, 46, 182, 21, 129, 92, 204, 90, 97, 9, 230, 2, 200, 131, 91, 164, 169, 252, 208, 216, 11, 241, 154, 41, 156, 236, 72, 120, 193, 199, 175, 49, 56, 78, 95, 115, 77, 232, 132, 209, 163, 96, 213, 48, 176, 112, 233, 218]


def substitution(input: b'', round_key: int):
    output = []
    for byte in input:
        # Die jeweiligen Substitutionen machen
        output.append(s_box[byte])
        pass
    # Int liste in bytes umwandeln und zurückgeben
    return bytes(output)


def encrypt_block(block: b'', keys: [int], rounds=16):
    # Linke und Rechte Hälfte aufteilen
    left = block[:len(block)//2]
    right = block[len(block)//2:]

    # Runden durchführen
    for current_round in range(0, rounds):
        left, right = encrypt_round(left, right, keys[current_round])
        pass

    # Zusammenfügen und zurückgeben
    return right + left
    pass


def encrypt_round(left: b'', right: b'', round_key: int):
    # Ausrechnen einer Runde
    # zuerst wird der Schlüssel auf die rechte Seite xor gemacht
    new_right = bytes([x ^ y for (x, y) in zip(
        right, round_key.to_bytes(8, 'big'))])
    # dann folgt die substitution der neuen rechten Seite
    new_right = substitution(right, round_key)
    # dann wird die linke seite auf die neue rechte Seite xor gemacht
    new_right = bytes([x ^ y for (x, y) in zip(new_right, left)])
    # die alte rechte Seite wird die neue linke Seite
    new_left = right

    return new_left, new_right
    pass


def getblocks(text: b'', length=128):
    # Den gegebenen Text in Blöcke teilen
    byte_length = length//8
    current_length = byte_length
    blocks = []

    # Trennen der Blöcke bis vielleicht etwas übersteht
    while current_length < len(text):
        blocks.append(text[current_length - byte_length: current_length])
        current_length += byte_length
        pass

    # Auffüllen mit nullen falls der letzte Block nicht vollständig ist
    if current_length > len(text):
        for i in range(0, current_length - len(text)):
            text = text + b'\x00'
            pass
        pass
        blocks.append(text[current_length - byte_length: current_length])
    pass
    return blocks


def leftshift(key: int, keylength: int, n: int):
    # Shiftfunktion da es keinen arithmetischen shift in python gibt
    bitmask = (2**n - 1) << keylength - n  # Bitmaske für die höchsten n Bits
    # Shift des Keys um obere Stellen wegzubekommen und dann nach unten um Bits anzuhängen
    return ((key & ~bitmask) << n) | ((key & bitmask) >> (keylength - n))
    pass


def permute(key: int, permutation: [int], keylength: int):
    # Gibt den permutierten Schlüssel zurück
    permuted = 0
    for index, permuted_index in enumerate(permutation):
        # Herausfinden des Bits an der Stelle des Index
        key_bit = (key >> keylength - 1 - index) & 1
        # Nun setzen wir das Bit an der Stelle die in der vorgegebenen Liste steht
        permuted = permuted | (key_bit << keylength - 1 - permuted_index)
    return permuted


def makeroundkeys(key=rand.randint(0, 2**64 - 1), rounds=16, keylength=64):
    # Key aufteilen in high und low
    key_high = key >> keylength//2
    key_low = key & (2**(keylength//2)-1)
    roundkeys = []

    # Roundkeys ausrechnen
    for i in range(0, rounds):

        # Keys shiften um 2
        key_high = leftshift(key_high, keylength//2, 2)
        key_low = leftshift(key_low, keylength//2, 2)

        # Keys zusammensetzen und permutieren
        key_permuted = permute((key_high << (keylength//2))
                               | key_low, permutation_list, keylength)
        roundkeys.append(key_permuted)
    pass

    return roundkeys
