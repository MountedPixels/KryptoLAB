import json


def encrypt(text: str, key: int, path: str):
    '''
    Verschlüsselt einen Text additiv mit dem gegebenen Schlüssel
    (Dabei wird Ascii verwendet)
    Speichert außerdem den Cryptotext im angegebenen Pfad
    '''
    crypto_text = ""

    # Schlüssel auf jedes Byte addieren (ein Buchstabe)
    for char in text:
        crypto_text = crypto_text + \
            chr((ord(char) + key) % 256)

    file = open(path + "/additive-crypto.txt", "w")
    file.write(crypto_text)
    file.close()

    return crypto_text


def decrypt(text: str, path: str):
    '''
    Entschlüsselt den angegebenen Text und speichert alle möglichen
    Texte in einer Datei ab
    '''

    struct = []
    for i in range(1, 255):
        clear_text = ""
        for char in text:
            clear_text = clear_text + chr((ord(char) - i) % 256)
        struct.append({"key": i, "text": clear_text[:50]})

    file = open(path + "/additive-break.json", "w")
    file.write(json.dumps(struct))
    file.close()

    return True
