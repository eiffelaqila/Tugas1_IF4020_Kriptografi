import struct

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
    for col in sorted_columns:
        for row in range(num_rows):
            if row < num_rows - 1 or (row == num_rows - 1 and col < num_columns - num_empty_cells):
                matrix[row][col] = ciphertext[k]
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

def encrypt_file(plaindata, key):
    # Encryption uses Extended Vigenere Cipher
    encrypted_bytes = bytearray()
    key_length = len(key)

    for i, datum in enumerate(plaindata):
        current_byte = int.from_bytes(datum, "big")
        key_byte = ord(key[i % key_length])

        encrypted_int = (current_byte + key_byte) % 256
        encrypted_bytes.append(encrypted_int)

    # Encrypt the results of the Extended Vigenere Cipher using 
    # Transposition Cipher
    num_columns = len(key)
    num_rows = -(-len(encrypted_bytes) // num_columns) # Rounding up division
    
    # Create a matrix to hold text
    matrix = [[0 for _ in range(num_columns)] for _ in range(num_rows)]
    for i, byte in enumerate(encrypted_bytes):
        matrix[i // num_columns][i % num_columns] = byte
    
    # Sorts columns according to key order
    sorted_columns = sorted(range(num_columns), key=lambda x: key[x])
    # Converts a matrix to encrypted text
    encrypted_bytes = list()
    for col in sorted_columns:
        for row in range(num_rows):
            encrypted_bytes.append(int.to_bytes(matrix[row][col], 1, "big"))
    return b"".join(encrypted_bytes)

def decrypt_file(cipherdata, key):
    # Decryption using Transposition Cipher
    num_columns = len(key)
    num_rows = -(-len(cipherdata) // num_columns)  # Rounding up division
    # Calculates the column index for each character in the key
    sorted_columns = sorted(range(num_columns), key=lambda x: key[x])

    # Converts encrypted text to a matrix
    matrix = [[0 for _ in range(num_columns)] for _ in range(num_rows)]
    # Mengisi matriks dengan teks terenkripsi secara berurutan
    k = 0
    for i in range(num_columns):
        col = sorted_columns[i]
        for j in range(num_rows):
            if (j < num_rows - 1 or (j == num_rows - 1)) and (k < len(cipherdata)):
                matrix[j][col] = int.from_bytes(cipherdata[k], "big")
                k += 1

    decrypted_bytes_tc = bytearray()
    for row in matrix:
        for byte_int in row:
            decrypted_bytes_tc.append(byte_int)
    
    decrypted_bytes_tc = decrypted_bytes_tc.rstrip(b'\x00')

    # Decrypt Transposition Cipher results using Extended Vigenere Cipher
    decrypted_bytes = list()
    key_length = len(key)

    for i, byte in enumerate(decrypted_bytes_tc):
        key_byte = ord(key[i % key_length])

        decrypted_int = (byte - key_byte) % 256
        decrypted_byte = int.to_bytes(decrypted_int, 1, "big")
        decrypted_bytes.append(decrypted_byte)
    
    return b"".join(decrypted_bytes)

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
    print()

    print("Mengenkripsi File Text")
    text_file = open('../../test/sample-text.txt', 'rb')
    data = text_file.read()
    data = struct.unpack("c" * (len(data)), data)
    encryptdata = encrypt_file(data, key)
    text_file.close()

    text_file = open('../../test/encrypted-sample-text.txt', 'wb')
    text_file.write(encryptdata)
    text_file.close()
    print("File Text Terenkripsi Telah Tersimpan")
    print()

    print("Mendekripsi File Text")
    text_file = open('../../test/encrypted-sample-text.txt', 'rb')
    data = text_file.read()
    data = struct.unpack("c" * (len(data)), data)
    decryptdata = decrypt_file(data, key)
    text_file.close()

    text_file = open('../../test/decrypted-sample-text.txt', 'wb')
    text_file.write(decryptdata)
    text_file.close()
    print("File Text Terdekripsi Telah Tersimpan")

    print("Mengenkripsi File Image")
    img_file = open('../../test/sample-img.jpg', 'rb')
    data = img_file.read()
    data = struct.unpack("c" * (len(data)), data)
    encryptdata = encrypt_file(data, key)
    img_file.close()

    img_file = open('../../test/encrypted-sample-img.jpg', 'wb')
    img_file.write(encryptdata)
    img_file.close()
    print("File Image Terenkripsi Telah Tersimpan")
    print()

    print("Mendekripsi File Image")
    img_file = open('../../test/encrypted-sample-img.jpg', 'rb')
    data = img_file.read()
    data = struct.unpack("c" * (len(data)), data)
    decryptdata = decrypt_file(data, key)
    img_file.close()

    img_file = open('../../test/decrypted-sample-img.jpg', 'wb')
    img_file.write(decryptdata)
    img_file.close()
    print("File Image Terdekripsi Telah Tersimpan")

    print("Mengenkripsi File Video")
    video_file = open('../../test/sample-video.mp4', 'rb')
    data = video_file.read()
    data = struct.unpack("c" * (len(data)), data)
    encryptdata = encrypt_file(data, key)
    video_file.close()

    video_file = open('../../test/encrypted-sample-video.mp4', 'wb')
    video_file.write(encryptdata)
    video_file.close()
    print("File Video Terenkripsi Telah Tersimpan")
    print()

    print("Mendekripsi File Video")
    video_file = open('../../test/encrypted-sample-video.mp4', 'rb')
    data = video_file.read()
    data = struct.unpack("c" * (len(data)), data)
    decryptdata = decrypt_file(data, key)
    video_file.close()

    video_file = open('../../test/decrypted-sample-video.mp4', 'wb')
    video_file.write(decryptdata)
    video_file.close()
    print("File Video Terdekripsi Telah Tersimpan")