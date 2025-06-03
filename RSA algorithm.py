def gcd(a, b):
    """Calculates the greatest common divisor of a and b using the Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """
    Implements the extended Euclidean algorithm.
    Returns (g, x, y) such that g = gcd(a, b) and ax + by = g.
    """
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def mod_inverse(a, m):
    """
    Calculates the modular multiplicative inverse of a modulo m.
    Raises ValueError if the inverse does not exist (gcd(a, m) != 1).
    """
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"Modular inverse does not exist (gcd({a}, {m}) = {g} ≠ 1).")
    return x % m

def mod_pow(base, exp, mod):
    """
    Calculates (base^exp) % mod efficiently using exponentiation by squaring.
    Includes detailed print statements for step-by-step understanding.
    """
    result = 1
    original_base_val = base # Store the initial base value for printing the final result
    base %= mod # Ensure base is within the modulo range
    
    print(f"  Calculating {original_base_val}^{exp} mod {mod} using Exponentiation by Squaring:")
    print(f"  Initial state: result = {result}, current_base_for_multiplication = {base}, current_exponent = {exp}")
    
    # Store steps to print later, ensuring clean output for intermediate values
    step_details = [] 
    
    while exp > 0:
        if exp & 1:  # If the last bit of exp is 1 (exp is odd)
            step_details.append(f"  Exponent is odd ({exp}): result = (result * current_base_for_multiplication) % mod = ({result} * {base}) % {mod} = {(result * base) % mod}")
            result = (result * base) % mod
        
        step_details.append(f"  Squaring current_base_for_multiplication: base = (current_base_for_multiplication * current_base_for_multiplication) % mod = ({base} * {base}) % {mod} = {(base * base) % mod}")
        base = (base * base) % mod
        
        step_details.append(f"  Dividing exponent by 2: exp = {exp} >> 1 = {exp >> 1}")
        exp >>= 1 # Right shift exp by 1 (equivalent to integer division by 2)
        step_details.append(f"  Current state: result = {result}, current_base_for_multiplication = {base}, current_exponent = {exp}")
        
    for detail in step_details:
        print(detail)
    
    print(f"  Final result of {original_base_val}^{exp} mod {mod} = {result}")
    return result

def solve_rsa_problem():
    """
    Solves an RSA problem with user input, including detailed steps for key generation,
    encryption, and decryption with speed optimization comments.
    """
    print("\n" + "="*25 + " RSA Problem Solver " + "="*25)
    p = int(input("Enter prime p: "))
    q = int(input("Enter prime q: "))
    e = int(input("Enter public exponent e: "))
    m = int(input("Enter plaintext M (0 < M < n): "))

    print("\n--- Step 1: Basic Calculations ---")
    n = p * q
    print(f"1. Modulus n = p * q = {p} * {q} = {n}")

    phi_n = (p - 1) * (q - 1)
    print(f"2. Euler's Totient Function φ(n) = (p - 1) * (q - 1) = ({p-1}) * ({q-1}) = {phi_n}")

    print("\n--- Step 2: Key Generation ---")
    # Adjust e if negative or outside valid range (1 < e < phi_n)
    original_e_input = e
    if e < 0: # Handle negative e
        e = e % phi_n
        if e < 0: # Ensure e is positive after modulo
            e += phi_n
        print(f"1. Original public exponent e = {original_e_input}. Adjusted e for 1 < e < φ(n): e = {e}")
    elif e >= phi_n: # Handle e larger than or equal to phi_n
        e = e % phi_n
        print(f"1. Original public exponent e = {original_e_input}. Adjusted e for 1 < e < φ(n): e = {e}")
    else: # e is valid initially
        print(f"1. Public exponent e = {e}")

    # Check if e is coprime to phi_n
    common_divisor = gcd(e, phi_n)
    if common_divisor != 1:
        raise ValueError(f"Error: e ({e}) and φ(n) ({phi_n}) must be coprime. Their GCD is {common_divisor}.")
    print(f"2. Check GCD(e, φ(n)): GCD({e}, {phi_n}) = {common_divisor}. (Must be 1 for inverse to exist)")

    # Calculate d
    print(f"3. Calculating private exponent d (e * d ≡ 1 mod φ(n)): {e} * d ≡ 1 mod {phi_n}")
    d = mod_inverse(e, phi_n)
    print(f"   d = {d}")

    print(f"\nPublic key KU = (e, n) = ({e}, {n})")
    print(f"Private key KR = (d, n) = ({d}, {n})")

    print("\n--- Step 3: Encryption ---")
    print(f"Plaintext M = {m}")
    print(f"Encryption C = M^e mod n = {m}^{e} mod {n}")
    print("Optimization: Using Exponentiation by Squaring for fast modular exponentiation.")
    c = mod_pow(m, e, n)
    print(f"Ciphertext C = {c}")

    print("\n--- Step 4: Decryption ---")
    print(f"Ciphertext C = {c}")
    print(f"Decryption M' = C^d mod n = {c}^{d} mod {n}")
    print("Optimization: Using Exponentiation by Squaring for fast modular exponentiation.")
    m_dec_pow = mod_pow(c, d, n)
    print(f"Decrypted plaintext M' (using direct modular exponentiation) = {m_dec_pow}")
    
    # Demonstrate CRT for decryption optimization
    print("\nDecryption Optimization: Using Chinese Remainder Theorem (CRT) for faster decryption.")
    print("  This is beneficial for large numbers as it breaks down one large exponentiation into two smaller ones.")
    dp = d % (p - 1)
    dq = d % (q - 1)
    print(f"  dp = d mod (p-1) = {d} mod ({p-1}) = {dp}")
    print(f"  dq = d mod (q-1) = {d} mod ({q-1}) = {dq}")

    mp = mod_pow(c, dp, p)
    mq = mod_pow(c, dq, q)
    print(f"  mp = C^dp mod p = {c}^{dp} mod {p} = {mp}")
    print(f"  mq = C^dq mod q = {c}^{dq} mod {q} = {mq}")

    # Apply CRT to combine results
    # CRT formula: M' = mq + q * ( (mp - mq) * (q_inv_p) ) mod n
    # Find q_inv_p = q^(-1) mod p
    q_inv_p = mod_inverse(q, p)
    print(f"  q_inv_p = q^(-1) mod p = {q}^(-1) mod {p} = {q_inv_p}")

    # Calculate intermediate component for CRT
    # x = (mp - mq) * q_inv_p mod p
    diff_mp_mq_mod_p = (mp - mq) % p # Ensure positive value
    if diff_mp_mq_mod_p < 0:
        diff_mp_mq_mod_p += p
    
    h = (diff_mp_mq_mod_p * q_inv_p) % p
    
    m_dec_crt = mq + h * q
    
    print(f"  Intermediate value (mp - mq) mod p = ({mp} - {mq}) mod {p} = {diff_mp_mq_mod_p}")
    print(f"  h = ((mp - mq) * q_inv_p) mod p = ({diff_mp_mq_mod_p} * {q_inv_p}) mod {p} = {h}")
    print(f"  Decrypted plaintext M' (using CRT) = mq + h * q = {mq} + {h} * {q} = {m_dec_crt}")

    print("\n--- Verification ---")
    if m_dec_pow == m and m_dec_crt == m:
        print(f"Decryption successful! Original M = {m}, Decrypted M' = {m_dec_pow} (or {m_dec_crt} via CRT).")
    else:
        print("Decryption failed. Please check calculations.")

# --- Run the problems ---
# To run each problem, you will need to input the corresponding values when prompted.

print("\nSolving Problem 1:")
# Input values for Problem 1: p=7, q=17, e=-11, M=20
solve_rsa_problem()

print("\n" + "="*70 + "\n") # Separator line

print("Solving Problem 2:")
# Input values for Problem 2: p=17, q=31, e=7, M=12
solve_rsa_problem()

print("\n" + "="*70 + "\n") # Separator line

print("Solving Problem 3:")
# Input values for Problem 3: p=5, q=11, e=7, M=26
solve_rsa_problem()