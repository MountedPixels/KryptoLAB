#####################################################
# Imports
import sys
import numpy as np
import math
import time
#####################################################


def main():
    if(sys.argv[1] == "-r"):
        calc_rauheitsgrad()
    if(sys.argv[1] == "-b"):
        calc_blocklength()
    if(sys.argv[1] == "-d"):
        decrypt()
    pass

def calc_occurence(clear, encrypted, blocks):
    #Verschlüsselter Text
    encrypted_matrix = [[0] *128 for x in range(blocks)]

    for pos_crypto, ep_clear in enumerate(encrypted):
        encrypted_matrix[pos_crypto % blocks][ord(ep_clear)] += 1
        pass
    
    #encrypted_matrix = [[x/(len(encrypted)/blocks) for x in array] for array in encrypted_matrix]

    # encrypted_array = [0] * 128

    # for i in range(0, 127):
    #     average = []
    #     for j in range(0, blocks - 1):
    #         average.append(encrypted_matrix[j][i])
    #         pass
    #     encrypted_array[i] = np.average(average)
    #     pass
     
    # print(encrypted_array)

    #Klartext wahrscheinlichkeiten
    clear_array = [0] *128

    for pos_crypto, ep_clear in enumerate(clear):
        clear_array[ord(ep_clear)] += 1
        pass
    
    #clear_array = [x/len(clear) for x in clear_array]

    max_clear = np.argmax(clear_array)

    key = []

    for array in encrypted_matrix:
        cryp_max = np.argmax(array)

        key.append((cryp_max - max_clear) % 128)
    
    key = ''.join(chr(x) for x in key)

    return key
    pass


def calc_rauheitsgrad():
    # input file
    read_filename = sys.argv[2]

    # read file
    text: str
    with open(read_filename, "r") as f:
        text = f.read()

    # liste mit allen möglichen chars
    char_array = [0] * 128

    # ocurences berechnen
    for i in text:
        char_array[ord(i)] += 1

    sum_p = 0
    # p(a) berechnen
    for i in range(0, len(char_array)):
        sum_p = sum_p + (char_array[i]/len(text))**2

    print(sum_p - 1/128)

def calc_rauheitsgrad(text):

    # liste mit allen möglichen chars
    char_array = [0] * 128

    # ocurences berechnen
    for i in text:
        char_array[ord(i)] += 1

    sum_p = 0
    # p(a) berechnen
    for i in range(0, len(char_array)):
        sum_p = sum_p + (char_array[i]/len(text))**2

    return(sum_p - 1/128)

def calc_blocklength():
    # input file
    read_filename = sys.argv[2]

    # read file
    text_input: str
    with open(read_filename, "r") as f:
        text_input = f.read()

    # berechnen der IC für die einzelnen Blocklängen
    ic_list = [0] * 100
    for _i in range(0, 100):
        i = _i + 1
        matrix_ic = [0]*i
        matrix = [""]*i

        for num, char in enumerate(text_input):
            matrix[num % i] += char

        # Berechnen der Matrizen nach Shema in der Vorlesung
        for num, colum in enumerate(matrix):
            char_table = [0] * 128
            for char in colum:
                char_table[ord(char)] += 1
            sum_chars = 0
            for j in char_table:
                sum_chars += j * (j-1)
            sum_chars = sum_chars * (1/(len(colum)*(len(colum)-1)))
            matrix_ic[num] = sum_chars
        ic_list[_i] = np.average(matrix_ic)

    max_ic = ic_list[0]
    max_ic_pos = 0
    for i, value in enumerate(ic_list):
        if(max_ic < value):
            max_ic = value
            max_ic_pos = i

    print(primfaktor(max_ic_pos + 1))
    return(primfaktor(max_ic_pos + 1))


def decrypt():
    # Cleartext einlesen um zu vergleichen bzw entschlüsseln.
    read_filename = sys.argv[3]

    # read file
    text_input_clear: str
    with open(read_filename, "r") as f:
        text_input_clear = f.read()

    text_input_clear_rh = calc_rauheitsgrad(text_input_clear)

    ####################
    # input file
    read_filename = sys.argv[2]

    # read file
    text_input: str
    with open(read_filename, "r") as f:
        text_input = f.read()

    blocks = calc_blocklength()
    _min = 1
    _key = ""
    _text = ""
    for i in blocks:
        key = calc_occurence(text_input_clear, text_input, i)
        text = ""
        for num, char in enumerate(text_input):
            text += chr((ord(char) - ord(key[num % i])) % 128)
        if(abs(calc_rauheitsgrad(text) - calc_rauheitsgrad(text_input_clear)) < _min):
            _min = abs(calc_rauheitsgrad(text) - calc_rauheitsgrad(text_input_clear))
            _key = key
            _text = text
    print(_text)
    print("Key: " + _key)


def zerlegung(pos, zahl, _max):
    if(zahl[pos] == 127):
        zahl[pos] = 0
        pos += 1
        if(pos > _max):
            return (pos, zahl, _max, False)
        zerlegung(pos, zahl, _max)
    else:
        zahl[pos] += 1
        pos = 0
    return (pos, zahl, _max, True)

def primfaktor(_n):
    n = _n

    p = 2
    liste = []
    while n != p:
        if n % p == 0:
            liste.append(p)
            n = n//p
        else:
            p += 1
    else:
        liste.append(p)
    in_list = 0
    new_list = []
    for i in liste:
        if(i > in_list):
            new_list.append(i)
            in_list = i
    new_list.append(_n)
    return new_list


main()
