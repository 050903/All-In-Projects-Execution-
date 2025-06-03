# MixColumns Matrix (Forward)
MIX_COL_MATRIX = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
]

# Inverse MixColumns Matrix
INV_MIX_COL_MATRIX = [
    [0x0E, 0x0B, 0x0D, 0x09],
    [0x09, 0x0E, 0x0B, 0x0D],
    [0x0D, 0x09, 0x0E, 0x0B],
    [0x0B, 0x0D, 0x09, 0x0E]
]

def mix_columns(state_matrix, matrix):
    """
    Performs MixColumns or InvMixColumns operation on a 4x4 state matrix.
    state_matrix: A 4x4 list of integers (bytes).
    matrix: The 4x4 MixColumns or InvMixColumns matrix.
    Returns: A new 4x4 state matrix.
    """
    if len(state_matrix) != 4 or any(len(row) != 4 for row in state_matrix):
        raise ValueError("State matrix must be 4x4.")

    new_state = [[0 for _ in range(4)] for _ in range(4)]

    for c in range(4): # For each column
        col_input = [state_matrix[r][c] for r in range(4)] # Get the current column

        for r in range(4): # Calculate each byte in the new column
            val = 0
            for i in range(4):
                # Multiply matrix[r][i] by col_input[i] in GF(2^8) and XOR to result
                val = val ^ gf_mul(matrix[r][i], col_input[i])  # XOR operation for GF(2^8) addition
            new_state[r][c] = val
    return new_state

def print_state_matrix(matrix, title=""):
    """Helper function to print a 4x4 matrix."""
    if title:
        print(title)
    for r in range(4):
        print(" ".join([f"{val:02X}" for val in matrix[r]]))
    print("-" * 30)

def gf_mul(a, b):
    """
    Perform multiplication in GF(2^8) using the Rijndael finite field.
    a, b: Integers (bytes) to multiply.
    Returns: Result of multiplication in GF(2^8).
    """
    p = 0
    for _ in range(8):
        if b & 1:  # If the lowest bit of b is set
            p ^= a  # XOR a into the result
        carry = a & 0x80  # Check if the highest bit of a is set
        a = (a << 1) & 0xFF  # Left shift a and keep it within 8 bits
        if carry:  # If there was a carry, XOR with the irreducible polynomial
            a ^= 0x1B
        b >>= 1  # Right shift b
    return p

# --- Ví dụ thực hiện MixColumns (Thuận) ---
print("\n--- Thao tác trộn cột (MixColumns) ---")

# Input state matrix from your slide (image_434d9a.jpg)
# Only showing the first column for clarity as the slide only details that.
# The full matrix from slide image_434d9a.jpg is:
input_state_mix_col = [
    [0x87, 0xF2, 0x4D, 0x97],
    [0x6E, 0x4C, 0x90, 0xEC],
    [0x46, 0xE7, 0x4A, 0xC3],
    [0xA6, 0x8C, 0xD8, 0x95]
]

print_state_matrix(input_state_mix_col, "Input State (MixColumns):")

output_state_mix_col = mix_columns(input_state_mix_col, MIX_COL_MATRIX)
print_state_matrix(output_state_mix_col, "Output State (MixColumns):")


# --- Ví dụ thực hiện InvMixColumns (Ngược) ---
print("\n--- Thao tác trộn cột ngược (InvMixColumns) ---")

# Input state for InvMixColumns is the output of MixColumns from slide image_434d9a.jpg
input_state_inv_mix_col = [
    [0x47, 0x40, 0xA3, 0x4C],
    [0x37, 0xD4, 0x70, 0x9F],
    [0x94, 0xE4, 0x3A, 0x42],
    [0xED, 0xA5, 0xA6, 0xBC]
]

print_state_matrix(input_state_inv_mix_col, "Input State (InvMixColumns):")

output_state_inv_mix_col = mix_columns(input_state_inv_mix_col, INV_MIX_COL_MATRIX)
print_state_matrix(output_state_inv_mix_col, "Output State (InvMixColumns):")

# Verification: The output of InvMixColumns should be the original input of MixColumns
print("\n--- Verification ---")
print("Original Input for MixColumns matches Output of InvMixColumns:",
      input_state_mix_col == output_state_inv_mix_col)