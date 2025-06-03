def shift_cipher_encrypt(plaintext, key):
    """Encrypts plaintext using a Caesar cipher (shift cipher)."""
    ciphertext = ""
    for char in plaintext:
        if 'A' <= char <= 'Z':
            shifted_char_ord = (ord(char) - ord('A') + key) % 26 + ord('A')
            ciphertext += chr(shifted_char_ord)
        elif 'a' <= char <= 'z':
            shifted_char_ord = (ord(char) - ord('a') + key) % 26 + ord('a')
            ciphertext += chr(shifted_char_ord)
        else:
            ciphertext += char
    return ciphertext

def monoalphabetic_encrypt(plaintext, key):
    """Encrypts plaintext using a monoalphabetic substitution cipher."""
    ciphertext = ""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.upper()
    mapping = str.maketrans(alphabet, key)
    ciphertext = plaintext.upper().translate(mapping)
    return ciphertext

if __name__ == "__main__":
    print("+-------------------------------------+")
    print("| 1. Shift Cipher (k = 15)          |")
    print("+-------------------------------------+")
    plaintext_shift = input("Enter plaintext for Shift Cipher: ").upper()
    key_shift = 15
    ciphertext_shift = shift_cipher_encrypt(plaintext_shift, key_shift)

    print(f"\nPlaintext: {plaintext_shift}")
    print(f"Key (k): {key_shift}")
    print(f"Ciphertext: {ciphertext_shift}")

    print("\n+-------------------------------------+")
    print("|   Module Operation for 'AN TOAN'    |")
    print("+-------------------------------------+")
    for char in "ANTOAN":
        if 'A' <= char <= 'Z':
            original_pos = ord(char) - ord('A')
            encrypted_pos = (original_pos + key_shift) % 26
            encrypted_char = chr(encrypted_pos + ord('A'))
            print(f"{char}: ({ord(char)} - {ord('A')} + {key_shift}) mod 26 = {encrypted_pos}, Encrypted: {encrypted_char}")
        else:
            print(f"{char}: Non-alphabetic character")

    print("\n+-------------------------------------+")
    print("| 2. Monoalphabetic Cipher          |")
    print("+-------------------------------------+")
    plaintext_mono = input("Enter plaintext for Monoalphabetic Cipher: ")
    key_mono = "DKVQFIBJWPESCXHTMYAUOLRGZN"
    ciphertext_mono = monoalphabetic_encrypt(plaintext_mono, key_mono)

    print(f"\nPlaintext: {plaintext_mono}")
    print(f"Key: {key_mono}")
    print(f"Ciphertext: {ciphertext_mono}")