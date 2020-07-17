import additive
import vigenere
import os

# Pfade deklarieren für einfacherere Nutzung
dir_path = os.path.dirname(os.path.realpath(__file__))
path = {
    "reference": {
        "constant": dir_path + "/reference/constant.txt",
        "lorem": dir_path + "/reference/lorem.txt",
        "random": dir_path + "/reference/random.txt"
    },
    "vigenere-crypto": {
        "lorem-cypto-1": dir_path + "/vigenere-crypto/lorem-crypto-1.txt",
        "lorem-cypto-2": dir_path + "/vigenere-crypto/lorem-crypto-2.txt",
        "lorem-cypto-3": dir_path + "/vigenere-crypto/lorem-crypto-3.txt",
        "lorem-cypto-4": dir_path + "/vigenere-crypto/lorem-crypto-4.txt"
    },
    "out": dir_path + "/out"
}


def main():
    file = open(path["reference"]["lorem"], "r")
    text = file.read()
    file.close()

    # Test additiv
    # test_additive(text)

    # Test vigenere
    # test_vigenere()

    pass


def test_additive(text: str):
    """
    Testet die additive chifre
    """
    crypto = additive.encrypt(text, 20, path["out"])
    additive.decrypt(crypto, path["out"])


def test_vigenere():
    file = open(path["reference"]["lorem"], "r")
    lorem_text = file.read()
    file.close()

    file = open(path["reference"]["random"], "r")
    random_text = file.read()
    file.close()

    file = open(path["reference"]["constant"], "r")
    constant_text = file.read()
    file.close()

    print("Rauheitsgrad Lorem: %s" %
          vigenere.calc_rauheitsgrad(lorem_text))
    print("Rauheitsgrad Random: %s" %
          vigenere.calc_rauheitsgrad(random_text))
    print("Rauheitsgrad Constant: %s" %
          vigenere.calc_rauheitsgrad(constant_text))

    for crypto_path in path["vigenere-crypto"]:
        file = open(path["vigenere-crypto"][crypto_path], "r")
        text = file.read()
        file.close()
        print("____________________")
        vigenere.decrypt(lorem_text, text)


if __name__ == "__main__":
    main()
