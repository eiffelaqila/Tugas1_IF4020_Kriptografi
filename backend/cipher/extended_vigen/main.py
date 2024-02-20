import struct

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

def encrypt_file(plaindata, key):
    encrypted_bytes = list()

    for i, datum in enumerate(plaindata):
        current_byte = int.from_bytes(datum, "big")
        key_byte = ord(key[i % len(key)])

        encrypted_int = (current_byte + key_byte) % 256
        encrypted_byte = int.to_bytes(encrypted_int, 1, "big")
        encrypted_bytes.append(encrypted_byte)

    return b"".join(encrypted_bytes)

def decrypt_file(cipherdata, key):
    decrypted_bytes = list()

    for i, datum in enumerate(cipherdata):
        current_byte = int.from_bytes(datum, "big")
        key_byte = ord(key[i % len(key)])

        decrypted_int = (current_byte - key_byte) % 256
        decrypted_byte = int.to_bytes(decrypted_int, 1, "big")
        decrypted_bytes.append(decrypted_byte)
    
    return b"".join(decrypted_bytes)     

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
    print()

    print("Mengenkripsi File")
    file = open('../../test/sample-img.jpg', 'rb')
    data = file.read()
    data = struct.unpack("c" * (len(data)), data)
    encryptdata = encrypt_file(data, key)
    file.close()

    file = open('../../test/encrypted-sample-img.jpg', 'wb')
    file.write(encryptdata)
    file.close()
    print("File Terenkripsi Telah Tersimpan")
    print()

    print("Mendekripsi File")
    file = open('../../test/encrypted-sample-img.jpg', 'rb')
    data = file.read()
    data = struct.unpack("c" * (len(data)), data)
    decryptdata = decrypt_file(data, key)
    file.close()

    file = open('../../test/decrypted-sample-img.jpg', 'wb')
    file.write(decryptdata)
    file.close()
    print("File Terdekripsi Telah Tersimpan")