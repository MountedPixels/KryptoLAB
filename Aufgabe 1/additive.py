def encrypt(text, key, m):
    internal = ""
    for char in text:
        internal = internal + \
            chr(((ord(char) - ord("A")) + key) % m + ord("A"))
    return internal


en = encrypt("HALLO", 123, 26)
print(en)
print(encrypt(en, -123, 26))
