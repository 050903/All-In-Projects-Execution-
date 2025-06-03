import numpy as np

def char_to_int(char):
    """Converts a character to its corresponding integer (A=0, B=1, ..., Z=25)."""
    return ord(char.upper()) - ord('A')

def int_to_char(num):
    """Converts an integer to its corresponding character."""
    return chr(num % 26 + ord('A'))

def prepare_plaintext(plaintext, m):
    """Prepares the plaintext by dividing it into blocks of size m."""
    plaintext = "".join(filter(str.isalpha, plaintext)).upper()
    padding_len = (m - (len(plaintext) % m)) % m
    plaintext += 'X' * padding_len
    return [plaintext[i:i + m] for i in range(0, len(plaintext), m)]

def create_key_matrix(key_str, m):
    """Creates the key matrix from the key string."""
    key_str = "".join(filter(str.isalpha, key_str)).upper()
    if len(key_str) != m * m:
        raise ValueError(f"Key length must be {m * m} characters for M = {m}.")
    key_matrix = np.array([char_to_int(char) for char in key_str]).reshape((m, m))
    return key_matrix

def hill_cipher_encrypt(plaintext, key_matrix, m):
    """Encrypts the plaintext using the Hill cipher."""
    ciphertext = ""
    blocks = prepare_plaintext(plaintext, m)
    for block in blocks:
        block_vector = np.array([[char_to_int(char)] for char in block])
        cipher_vector = np.dot(key_matrix, block_vector) % 26
        ciphertext += "".join([int_to_char(val[0]) for val in cipher_vector])
    return ciphertext

def inverse_matrix(matrix):
    """Calculates the inverse of the matrix modulo 26."""
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = -1
    for i in range(26):
        if (det * i) % 26 == 1:
            det_inv = i
            break
    if det_inv == -1:
        raise ValueError("Determinant has no modular inverse mod 26. Matrix is not invertible.")

    adjugate = np.round(det * np.linalg.inv(matrix)).astype(int)
    return (det_inv * adjugate) % 26

def hill_cipher_decrypt(ciphertext, inverse_key_matrix, m):
    """Decrypts the ciphertext using the Hill cipher."""
    plaintext = ""
    blocks = [ciphertext[i:i + m] for i in range(0, len(ciphertext), m)]
    for block in blocks:
        block_vector = np.array([[char_to_int(char)] for char in block])
        plain_vector = np.dot(inverse_key_matrix, block_vector) % 26
        plaintext += "".join([int_to_char(val[0]) for val in plain_vector])
    return plaintext.rstrip('X')

if __name__ == "__main__":
    print("Hill Cipher Program")

    # Exercise 1
    print("\nExercise 1: Encrypt the word JULY (M = 2)")
    plaintext1 = input("Enter plaintext (e.g., JULY): ")
    key_str1 = input("Enter key (e.g., LDIH): ")
    m1 = 2

    try:
        key_matrix1 = create_key_matrix(key_str1, m1)
        print(f"Key Matrix:\n{key_matrix1}")

        inverse_key_matrix1 = inverse_matrix(key_matrix1)
        print(f"Inverse Key Matrix:\n{inverse_key_matrix1}")

        ciphertext1 = hill_cipher_encrypt(plaintext1, key_matrix1, m1)
        print(f"Plaintext: {plaintext1}")
        print(f"Ciphertext: {ciphertext1}")

        decrypted_text1 = hill_cipher_decrypt(ciphertext1, inverse_key_matrix1, m1)
        print(f"Decrypted Plaintext: {decrypted_text1}")
    except ValueError as e:
        print(f"Error: {e}")
    except np.linalg.LinAlgError:
        print("Error: Key matrix is not invertible (determinant is zero).")

    # Exercise 2
    print("\nExercise 2: Encrypt and decrypt the plaintext 'ACT' (M = 3)")
    plaintext2 = input("Enter plaintext (e.g., ACT): ")
    key_str2 = input("Enter key (9 characters, e.g., GYBNQURVK): ")
    m2 = 3

    try:
        key_matrix2 = create_key_matrix(key_str2, m2)
        print(f"Key Matrix:\n{key_matrix2}")

        inverse_key_matrix2 = inverse_matrix(key_matrix2)
        print(f"Inverse Key Matrix:\n{inverse_key_matrix2}")

        ciphertext2 = hill_cipher_encrypt(plaintext2, key_matrix2, m2)
        print(f"Plaintext: {plaintext2}")
        print(f"Ciphertext: {ciphertext2}")

        decrypted_text2 = hill_cipher_decrypt(ciphertext2, inverse_key_matrix2, m2)
        print(f"Decrypted Plaintext: {decrypted_text2}")
    except ValueError as e:
        print(f"Error: {e}")
    except np.linalg.LinAlgError:
        print("Error: Key matrix is not invertible (determinant is zero).")
