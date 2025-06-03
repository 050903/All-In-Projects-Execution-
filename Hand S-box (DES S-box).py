# DES S-box S1 from your slide (image_435958.jpg)
S1_BOX = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
]

def des_sbox_lookup(input_6_bit_str):
    """
    Performs a DES S-box lookup for S1.
    input_6_bit_str: A string of 6 bits (e.g., "101100").
    Returns: A string of 4 bits.
    """
    if len(input_6_bit_str) != 6 or not all(b in '01' for b in input_6_bit_str):
        raise ValueError("Input must be a 6-bit string.")

    # Step 1: Get row bits (first and last)
    row_bits_str = input_6_bit_str[0] + input_6_bit_str[5]
    row = int(row_bits_str, 2)

    # Step 2: Get column bits (middle 4 bits)
    col_bits_str = input_6_bit_str[1:5]
    col = int(col_bits_str, 2)

    print(f"Input: {input_6_bit_str}")
    print(f"  Row bits: {row_bits_str} (Decimal: {row})")
    print(f"  Col bits: {col_bits_str} (Decimal: {col})")

    # Step 3: Lookup value in S1_BOX
    sbox_value = S1_BOX[row][col]
    print(f"  Value from S-box (Row {row}, Col {col}): {sbox_value}")

    # Step 4: Convert to 4-bit binary string
    output_4_bit_str = format(sbox_value, '04b')
    print(f"  Output 4-bit: {output_4_bit_str}")
    print("-" * 30)
    return output_4_bit_str

# --- Ví dụ thực hiện ---
print("--- Chạy tay S-box (DES S1) ---")
des_sbox_lookup("101100") # Example from your slide
des_sbox_lookup("010111") # My example from previous explanation
des_sbox_lookup("110001") # Another example