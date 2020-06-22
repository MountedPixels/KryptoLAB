crpt = "NYRK RIV KYV JVMVEKY REU VZXYKY TYRIRTKVIJ FW PFLI LEZMVIJZKP VDRZC RUUIVJJ"
# crpt = "ATEEH"


def encrypt(text, key, m):
    internal = ""
    for char in text:
        if(char == " "):
            internal = internal + " "
        else:
            internal = internal + \
                chr(((ord(char) - ord("A")) + key) % m + ord("A"))
    return internal


for i in range(0, 26):
    print(encrypt(crpt, -i, 26))

print(encrypt(crpt, -17, 26))
