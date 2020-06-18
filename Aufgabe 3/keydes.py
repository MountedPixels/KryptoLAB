import sys
import random as rand

permutation = [39, 46, 57, 29, 50, 36, 14, 8, 45, 31, 53, 21, 56, 55, 32, 30, 16, 38, 47, 37, 7, 5, 27, 49, 48, 58, 26, 42, 60, 23, 12, 44, 24, 17, 6, 54, 2, 34, 62, 35, 22, 15, 4, 43, 40, 11, 51, 52, 1, 33, 28, 61, 18, 13, 59, 19, 0, 41, 20, 10, 3, 9, 25, 63]

def keyround(key1, key2):

    # Keys zusammenfügen
    key1 = key1 << 32
    togetherkey = key1 | key2
    finalkey = 0

    # Anwenden der Permutation durch bitweise Operation und Masken
    for i in range(0,63):
        mask = 2**i
        bit = togetherkey & mask
        if(i >= permutation[i]):
            bit = bit >> (abs(permutation[i] - i))
            pass
        else:
            bit = bit << (abs(permutation[i] - i))
            pass
        finalkey = finalkey | bit
        pass

    return finalkey
    pass

def leftshift(position, key):
    # Shiftfunktion da es keinen arithmetischen shift in python gibt
    mask = 0
    for i in range(64 - position, 63):
        mask += 2**i
        pass
    first2bits = mask & key
    key = key << position
    key = (mask >> 62) | key
    return key
    pass

def makeroundkeys(key, rounds):
    # Key aufteilen in links und rechts
    key1 = key >> 32
    key2 = key & ((2**32 - 1) << 32)
    roundkeys = []

    # Roundkeys ausrechnen
    for i in range (0,rounds):

        # Keys shiften um 2
        key1 = leftshift(2,key1)
        key2 = leftshift(2,key2)

        roundkeys.append(keyround(key1,key2))
        pass


    return roundkeys

key = rand.randint(0, 2**64 - 1)

print("Key: %s" % key)
print("Roundkeys:")
print(makeroundkeys(key, 16))