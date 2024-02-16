def encrypt(plaintext, key):
    """
    Returns the Auto-Key Vigenère encryption result of 
    the text specified with the given key.
    """
    plaintext = plaintext.upper()
    key = key.upper()
    ciphertext = ''
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            # Gets the ASCII value of the plaintext letter and key
            plaintext_char = ord(char) - ord('A')
            key_char = ord(key[key_index]) - ord('A')
            
            # Encrypts plaintext characters
            encrpyted_char = (plaintext_char + key_char) % 26

            # Adds encrypted characters to encrypted text
            ciphertext += chr(encrpyted_char + ord('A'))

            # Adds characters to a key to generate a key stream
            key += char
            key_index += 1            
    
    return ciphertext

def decrypt(ciphertext, key):
    """
    Returns the Vigenère decryption result of 
    the specified ciphertext with the given key.
    """
    ciphertext = ciphertext.upper()
    key = key.upper()
    decrypted_text = ''
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            # Gets the ASCII value of the plaintext letter and key
            ciphertext_char = ord(char) - ord('A')
            key_char = ord(key[key_index]) - ord('A')

            # Decrypts ciphertext characters
            decrypted_char = (ciphertext_char - key_char) % 26

            # Adds encrypted characters to decrypted text
            decrypted_text += chr(decrypted_char + ord('A'))

            # Adds characters to the key to generate a key stream
            key += chr(decrypted_char + ord('A'))
            key_index += 1

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