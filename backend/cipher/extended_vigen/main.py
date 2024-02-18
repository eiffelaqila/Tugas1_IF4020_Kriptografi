def encrypt(plaintext, key):
    encrypted_text = ''

    for i, char in enumerate(plaintext):
        # Convert plaintext characters and keys to ASCII values
        plaintext_char = ord(char)
        key_char = ord(key[i % len(key)])

        # Encrypt plaintext characters
        encrypted_char = (plaintext_char + key_char) % 256

        # Adds encrypted characters to encrypted text
        encrypted_text += chr(encrypted_char)
    
    return encrypted_text

def decrypt(ciphertext, key):
    decrypted_text = ''

    for i, char in enumerate(ciphertext):
        # Converts ciphertext characters and keys to ASCII values
        ciphertext_char = ord(char)
        key_char = ord(key[i % len(key)])

        # Decrypts ciphertext characters
        decrypted_char = (ciphertext_char - key_char) % 256

        # Adds decrypted characters to the decrypted text
        decrypted_text += chr(decrypted_char)

    return decrypted_text        

if __name__ == "__main__":
    plaintext = "Ini adalah pesan rahasia 1."
    key = "kunci"
    ciphertext = encrypt(plaintext, key)
    print("Plaintext:", plaintext)
    print("Kunci:", key)
    print("Teks Terenkripsi:", ciphertext)
    print()

    decrypted_text = decrypt(ciphertext, key)
    print("Ciphertext:", ciphertext)
    print("Kunci:", key)
    print("Teks Terdekripsi:", decrypted_text)