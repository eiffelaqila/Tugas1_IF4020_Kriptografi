def encrypt(plaintext, key):
    # Encryption uses Extended Vigenere Cipher
    encrypted_text = ""
    key_length = len(key)

    for i, char in enumerate(plaintext):
        key_char = key[i % key_length]
        # Encrypt plaintext characters using the appropriate key
        encrypted_char = chr((ord(char) + ord(key_char)) % 256)
        encrypted_text += encrypted_char
    
    # Encrypt the results of the Extended Vigenere Cipher using 
    # Transposition Cipher
    num_columns = len(key)
    num_rows = -(-len(plaintext) // num_columns) # Rounding up division
    
    # Create a matrix to hold text
    matrix = [['' for _ in range(num_columns)] for _ in range(num_rows)]
    for i, char in enumerate(encrypted_text):
        matrix[i // num_columns][i % num_columns] = char
    
    # Sorts columns according to key order
    sorted_columns = sorted(range(num_columns), key=lambda x: key[x])
    # Converts a matrix to encrypted text
    encrypted_text = ''
    for col in sorted_columns:
        for row in range(num_rows):
            encrypted_text += matrix[row][col]
    return encrypted_text

def decrypt(ciphertext, key):
    # Decryption using Transposition Cipher
    num_columns = len(key)
    num_rows = -(-len(ciphertext) // num_columns) # Rounding up division
    # Counts the number of unfilled cells in the last row of the matrix
    num_empty_cells = num_rows * num_columns - len(ciphertext)
    # Calculates the column index for each character in the key
    sorted_columns = sorted(range(num_columns), key=lambda x: key[x])

    # Converts encrypted text to a matrix
    matrix = [['' for _ in range(num_columns)] for _ in range(num_rows)]
    # Mengisi matriks dengan teks terenkripsi secara berurutan
    k = 0
    for i in range(num_columns):
        col = sorted_columns[i]
        for j in range(num_rows):
            if j < num_rows - 1 or (j == num_rows - 1 and col + 1 < num_empty_cells):
                matrix[j][col] = ciphertext[k]
                k += 1

    decrypted_text_tc = ''
    for row in matrix:
        for char in row:
            decrypted_text_tc += char

    # Decrypt Transposition Cipher results using Extended Vigenere Cipher
    decrypted_text = ""
    key_length = len(key)
    
    for i, char in enumerate(decrypted_text_tc):
        key_char = key[i % key_length]
        # Mendekripsi karakter ciphertext menggunakan kunci yang sesuai
        decrypted_char = chr((ord(char) - ord(key_char)) % 256)
        decrypted_text += decrypted_char
    
    return decrypted_text

if __name__ == "__main__":
    plaintext = "Ini adalah pesan rahasia 1."
    key = "kunci"
    ciphertext = encrypt(plaintext, key)
    print("Plaintext:", plaintext)
    print(f"Kunci: {key}")
    print("Teks Terenkripsi:", ciphertext)
    print()

    decrypted_text = decrypt(ciphertext, key)
    print("Ciphertext:", ciphertext)
    print("Kunci:", key)
    print("Teks Terdekripsi:", decrypted_text)