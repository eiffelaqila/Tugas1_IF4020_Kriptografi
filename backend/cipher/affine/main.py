def encrypt(plaintext, a, b):
    plaintext = plaintext.upper()
    encrypted_text = ""
    
    for char in plaintext:
        if char.isalpha():
            # Convert letters into numbers 0-25
            char_index = ord(char) - ord('A')
            # Encryption uses the affine cipher formula: E(x) = (ax + b) mod 26
            encrypted_index = (a * char_index + b) % 26
            # Converts the encrypted index back to letters
            encrypted_text += chr(encrypted_index + ord('A'))
    
    return encrypted_text

def decrypt(ciphertext, a, b):
    ciphertext = ciphertext.upper()
    decrypted_text = ''

    # Find the inverse modulo of a
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        raise Exception("Tidak bisa melakukan dekripsi: kunci tidak valid")

    for char in ciphertext:
        if char.isalpha():
            # Convert letters into numbers 0-25
            char_index = ord(char) - ord('A')
            # Decryption using the affine cipher formula: D(x) = a_inv * (x - b) mod 26
            decrypted_index = (a_inv * (char_index - b)) % 26
            # Converts the encrypted index back to letters
            decrypted_text += chr(decrypted_index + ord('A'))
    
    return decrypted_text

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

if __name__ == "__main__":
    plaintext = "Ini adalah pesan rahasia 1."
    a = 5
    b = 8
    ciphertext = encrypt(plaintext, a, b)
    print("Plaintext:", plaintext)
    print(f"Kunci: a = {a}, b = {b}")
    print("Teks Terenkripsi:", ciphertext)
    print()

    decrypted_text = decrypt(ciphertext, a, b)
    print("Ciphertext:", ciphertext)
    print(f"Kunci: a = {a}, b = {b}")
    print("Teks Terdekripsi:", decrypted_text)