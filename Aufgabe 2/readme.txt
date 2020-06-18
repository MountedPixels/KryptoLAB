Benutzung:
###############################################

python vigenere.py -r "Text.txt"
---------------------
Berechnet den Rauheitsgrad des gegebenen Text und gibt ihn aus.

python vigenere.py -b "Encrypted.txt"
---------------------
Errechnet die Blocklänge d mit Hilfe des Algorithmus aus der Vorlesung. (Koinzidenzindex-Untersuchungen)
Mir ist hierbei jedoch aufgefallen, das wenn nach dem Maximum gesucht wird, es dazu komme kann
das ein vielfaches der eigentlichen Blocklänge erkannt wird. Dies gibt also die Primfaktorzerlegung 
und die Zahl selbs in einer Liste aus

python vigenere.py -d "Encrypted.txt" "Plain.txt"
---------------------
Berechnet mit hilfe eines Sprachbeispiels den Schlüssel und gibt den entschlüsselten Text aus.


