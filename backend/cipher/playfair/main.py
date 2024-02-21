import re

def encrypt(plaintext, key):
    plaintext = prepare_input(plaintext)
    key_matrix = generate_key_matrix(key)
    encrypted_text = ""

    for i in range(0, len(plaintext), 2):
        char1 = plaintext[i]
        char2 = plaintext[i+1]
        row1, col1 = find_position(key_matrix, char1)
        row2, col2 = find_position(key_matrix, char2)

        if row1 == row2:
            encrypted_text += key_matrix[row1][(col1 + 1) % 5]
            encrypted_text += key_matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted_text += key_matrix[(row1 + 1) % 5][col1]
            encrypted_text += key_matrix[(row2 + 1) % 5][col2]
        else:
            encrypted_text += key_matrix[row1][col2]
            encrypted_text += key_matrix[row2][col1]
        
    return encrypted_text

def decrypt(ciphertext, key):
    ciphertext = "".join(re.split("[^A-Z]*", ciphertext.upper()))
    key_matrix = generate_key_matrix(key)
    decrypted_text = ""

    for i in range(0, len(ciphertext), 2):
        char1 = ciphertext[i]
        char2 = ciphertext[i + 1]
        row1, col1 = find_position(key_matrix, char1)
        row2, col2 = find_position(key_matrix, char2)

        if row1 == row2:
            decrypted_text += key_matrix[row1][(col1 - 1) % 5]
            decrypted_text += key_matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            decrypted_text += key_matrix[(row1 - 1) % 5][col1]
            decrypted_text += key_matrix[(row2 - 1) % 5][col2]
        else:
            decrypted_text += key_matrix[row1][col2]
            decrypted_text += key_matrix[row2][col1]
    
    return decrypted_text

def prepare_input(text):
    # Cleans text from non-alphabetic characters and converts to uppercase
    text = "".join(re.split("[^A-Z]*", text.upper()))
    # Replacing the letter 'j' with 'i'
    text = text.replace("J", "I")
    
    # Separates paired letters with 'x' if there are two of the same letters 
    # side by side
    clean_text = ""
    i = 0
    while i < len(text):
        clean_text += text[i]
        if i < len(text) - 1 and text[i] == text[i+1]:
            clean_text += 'X'
        i += 1
    
    # If the number of letters in the text is odd, add 'x' at the end
    if len(clean_text) % 2 == 1:
        clean_text += 'X'

    return clean_text

def generate_key_matrix(key):
    # Convert key to uppercase
    key = key.upper().replace(" ", "")
    # Removes duplicate characters from a key and letter 'j'
    key = "".join(dict.fromkeys(key)).replace('J', '')
    # Create a 5x5 matrix to hold the keys
    key_matrix = [['' for _ in range(5)] for _ in range(5)]

    # Filling the matrix with key letters
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    k = 0
    for i in range(5):
        for j in range(5):
            if k < len(key):
                key_matrix[i][j] = key[k]
                alphabet = alphabet.replace(key[k], "")
                k += 1
            else:
                key_matrix[i][j] = alphabet[0]
                alphabet = alphabet[1:]
    
    return key_matrix

def find_position(matrix, char):
    # Finds the character's position in the matrix
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j

if __name__ == "__main__":
    plaintext = "Ini adalah pesan rahasia 1."
    key = "playfair example"
    ciphertext = encrypt(plaintext, key)
    print("Plaintext:", plaintext)
    print("Kunci:", key)
    print("Teks Terenkripsi:", ciphertext)
    print()

    decrypted_text = decrypt(ciphertext, key)
    print("Ciphertext:", ciphertext)
    print("Kunci:", key)
    print("Teks Terdekripsi:", decrypted_text)