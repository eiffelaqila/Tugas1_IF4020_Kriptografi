ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ROTORS = {
    "I": ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"],
    "II": ["AJDKSIRUXBLHWTMCQGZNPYFVOE", "E", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"],
    "III": ["BDFHJLCPRTXVZNYEIWGAKMUSQO", "V", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"],
    "IV": ["ESOVPZJAYQUIRHXLNFTGKDCMWB", "J", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"],
    "V": ["VZBRGITYUPSDNHLXAWMJQOFECK", "Z", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
}
REFLECTORS = {
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
}

# REFLECTOR
def get_reflector(reflector, signal):
    letter = ALPHABET[signal]
    return reflector.find(letter)

# ROTOR
def get_rotor(rotor, signal, isForward=True):
    if (isForward):
        letter = rotor[0][signal]
        return rotor[2].find(letter)
    else:
        letter = rotor[2][signal]
        return rotor[0].find(letter)

def rotate_rotor(rotor, n=1):
    for i in range(n):
        rotor[0] = rotor[0][1:] + rotor[0][0]
        rotor[2] = rotor[2][1:] + rotor[2][0]
    return rotor

def rotate_rotor_to_letter(rotor, letter):
    letter = ALPHABET.find(letter)
    return rotate_rotor(rotor, letter)

def set_rotor_ring(rotor, n):
    for i in range(n):
        rotor[0] = rotor[0][25] + rotor[0][:25]
        rotor[2] = rotor[2][25] + rotor[2][:25]

    rotor[1] = ALPHABET[((ALPHABET.find(rotor[1]) - n) % 26)]

    return rotor

# PLUGBOARD
def setup_plugboard(pairs):
    plugboard = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if (pairs != [""]):
        for pair in pairs:
            idx1 = plugboard.find(pair[0])
            idx2 = plugboard.find(pair[1])
            plugboard = plugboard[:idx1] + pair[1] + plugboard[idx1+1:]
            plugboard = plugboard[:idx2] + pair[0] + plugboard[idx2+1:]
        
    return plugboard

def get_plugboard(plugboard, signal, isForward=True):
    if (isForward):
        letter = ALPHABET[signal]
        return plugboard.find(letter)
    else:
        letter = plugboard[signal]
        return ALPHABET.find(letter)


def enigma(
    plaintext,
    reflector,
    rotors,
    rings,
    positions,
    pairs,
):
    plaintext = plaintext.upper()
    ciphertext = ""

    pairs = pairs.split(",")
    plugboard = setup_plugboard(pairs)

    rotor1 = ROTORS[rotors[0]].copy()
    rotor1 = set_rotor_ring(rotor1, ALPHABET.find(rings[0]))
    rotor1 = rotate_rotor_to_letter(rotor1, positions[0])
    rotor2 = ROTORS[rotors[1]].copy()
    rotor2 = set_rotor_ring(rotor2, ALPHABET.find(rings[1]))
    rotor2 = rotate_rotor_to_letter(rotor2, positions[1])
    rotor3 = ROTORS[rotors[2]].copy()
    rotor3 = set_rotor_ring(rotor3, ALPHABET.find(rings[2]))
    rotor3 = rotate_rotor_to_letter(rotor3, positions[2])
    
    for char in plaintext:
        if char.isalpha():
            if rotor2[2][0] == rotor2[1] and rotor3[2][0] == rotor3[1]:
                rotate_rotor(rotor1)
                rotate_rotor(rotor2)
                rotate_rotor(rotor3)
            elif rotor2[2][0] == rotor2[1]:
                rotate_rotor(rotor1)
                rotate_rotor(rotor2)
                rotate_rotor(rotor3)
            elif rotor3[2][0] == rotor3[1]:
                rotate_rotor(rotor2)
                rotate_rotor(rotor3)
            else:
                rotate_rotor(rotor3)

            signal = ALPHABET.find(char)
            signal = get_plugboard(plugboard, signal)
            signal = get_rotor(rotor3, signal)
            signal = get_rotor(rotor2, signal)
            signal = get_rotor(rotor1, signal)
            signal = get_reflector(REFLECTORS[reflector], signal)
            signal = get_rotor(rotor1, signal, False)
            signal = get_rotor(rotor2, signal, False)
            signal = get_rotor(rotor3, signal, False)
            signal = get_plugboard(plugboard, signal, False)

            ciphertext += ALPHABET[signal]
        
    return ciphertext

if __name__ == "__main__":
    plaintext = "Ini adalah pesan rahasia 1."
    reflector = "B"
    rotors = ["IV", "II", "I"]
    rings = ["A", "A", "B"]
    positions = ["C", "A", "T"]
    pairs = "AB,CD,EF"
    ciphertext = enigma(
        plaintext,
        reflector,
        rotors,
        rings,
        positions,
        pairs,
    )

    print("Plaintext:", plaintext)
    print("Reflector:", reflector)
    print("Rotors:", rotors)
    print("Rings:", rings)
    print("Positions:", positions)
    print("Pairs:", pairs)
    print("Teks Terenkripsi:", ciphertext)
    print()

    decrypted_text = enigma(
        ciphertext,
        reflector,
        rotors,
        rings,
        positions,
        pairs,
    )
    print("Ciphertext:", ciphertext)
    print("Reflector:", reflector)
    print("Rotors:", rotors)
    print("Rings:", rings)
    print("Positions:", positions)
    print("Pairs:", pairs)
    print("Teks Terdekripsi:", decrypted_text)
    print()