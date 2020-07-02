import sys
import random as rand

permutation_list = [39, 46, 57, 29, 50, 36, 14, 8, 45, 31, 53, 21, 56, 55, 32, 30, 16, 38, 47, 37, 7, 5, 27, 49, 48, 58, 26, 42, 60,
                    23, 12, 44, 24, 17, 6, 54, 2, 34, 62, 35, 22, 15, 4, 43, 40, 11, 51, 52, 1, 33, 28, 61, 18, 13, 59, 19, 0, 41, 20, 10, 3, 9, 25, 63]


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
        print(bin(key_high))

        # Keys zusammensetzen und permutieren
        key_permuted = permute((key_high << (keylength//2))
                               | key_low, permutation_list, keylength)
        roundkeys.append(key_permuted)
    pass

    return roundkeys


key = int("0000111100001111000011110000111100001111000011110000111100001111", 2)

print("Key: %s" % key)

for pos, round_key in enumerate([bin(x) for x in makeroundkeys(key=key, rounds=2, keylength=64)]):
    while len(round_key) < 66:
        round_key = round_key[:2] + "0" + round_key[2:]
    print("Roundkey %s:" % pos)
    print(round_key)
