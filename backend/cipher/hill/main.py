import numpy as np 

def encrypt(plaintext, key):
    # Gets the block size (n x n) of the key
    n = int(np.sqrt(len(key)))
    plaintext = prepare_input(plaintext, n)
    key_matrix = np.array(text_to_matrix(key.upper())).reshape(n, n)
    encrypted_text = ''

    for i in range(0, len(plaintext), n):
        # Text matrix
        text_matrix = np.array(text_to_matrix(plaintext[i:i+n])).reshape(n, 1)
        # Encryption: C = K * P mod 26
        encrypted_matrix = np.dot(key_matrix, text_matrix) % 26
        # Converts an encrypted matrix to text
        encrypted_text += matrix_to_text(encrypted_matrix)
    
    return encrypted_text

def decrypt(ciphertext, key):
    # Gets the block size (n x n) of the key
    n = int(np.sqrt(len(key)))
    key_matrix = np.array(text_to_matrix(key.upper())).reshape(n, n)
    decrypted_text = ""

    # Find the inverse modulo of the key determinant
    determinant = int(round(np.linalg.det(key_matrix)))
    determinant_inverse = mod_inverse(determinant % 26, 26)   

    if determinant_inverse is None:
        return "Tidak bisa melakukan dekripsi: kunci tidak valid"

    # Finds the inverse of the key
    key_inverse = (determinant_inverse * np.round(determinant * np.linalg.inv(key_matrix))).astype(int) % 26 

    for i in range(0, len(ciphertext), n):
        # Encrypted text matrix
        text_matrix = np.array(text_to_matrix(ciphertext[i:i + n])).reshape(n, 1)
        # Decryption: P = K^(-1) * C mod 26
        decrypted_matrix = np.dot(key_inverse, text_matrix) % 26
        # Converts the decrypted matrix to text
        decrypted_text += matrix_to_text(decrypted_matrix)

    return decrypted_text

def prepare_input(plaintext, n):
    # Converts text to uppercase and removes non-alphabetic characters
    plaintext = ''.join(filter(str.isalpha, plaintext.upper()))

    # Adds the letter 'x' if the text length does not match the block length
    if len(plaintext) % n != 0:
        plaintext += 'X' * (n - len(plaintext) % n)

    return plaintext

def text_to_matrix(text):
    # Convert text to matrix with alphabet values (0-25)
    return [ord(char) - ord('A') for char in text]

def matrix_to_text(matrix):
    # Convert matrix to text with alphabet values (0-25)
    return ''.join([chr(int(char) % 26 + ord('A')) for sublist in matrix for char in sublist])

def mod_inverse(a, m):
    # Finding the inverse modulo using the Euclidean algorithm
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

if __name__ == "__main__":
    plaintext = "Ini adalah pesan rahasia 1."
    key = "tsnv"
    ciphertext = encrypt(plaintext, key)
    print("Plaintext:", plaintext)
    print("Kunci:", key)
    print("Teks Terenkripsi:", ciphertext)
    print()

    decrypted_text = decrypt(ciphertext, key)
    print("Ciphertext:", ciphertext)
    print("Kunci:", key)
    print("Teks Terdekripsi:", decrypted_text)