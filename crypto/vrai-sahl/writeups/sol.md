# Vrai Sahl CTF Writeup

## Challenge Overview

- **CTF**: Ingeneer
- **Challenge**: Vrai Sahl
- **Category**: Crypto
- **Points**: Hard
- **Description**: I didn't have much time, so I made an easy challenge but labeled it hard—kind of like calling a first-year spell a N.E.W.T.-level exam. Sorry for the mix-up! 

## TL;DR

This challenge presented a hybrid encryption scheme combining RSA and Elliptic Curve Cryptography (ECC). The primary vulnerability lay in the RSA prime generation, where a significant portion of the least significant bits (LSBs) of both prime factors was generated using a predictable pattern. This allowed for a partial reconstruction of the primes using a brute-force approach on the second nibble of each byte. Once enough bits of the RSA primes were recovered, Coppersmith's method was applied to find the remaining unknown high bits. With one of the RSA primes fully recovered, the flag, which was hidden as a common root of two polynomials (one derived from the hybrid encryption and another from the ECC point doubling formula), was found by computing the GCD of these polynomials.

## Initial Analysis

The challenge source code `main.py` reveals a multi-layered encryption process:

```python
from Crypto.Util.number import *
from random import *
from sage.all import *

def generate_custom_prime():
    while True:
        suffix = str(getRandomNBitInteger(140)).encode().hex()[2:]
        prefix = hex(getRandomNBitInteger(100))[2:]
        candidate = int(prefix + suffix, 16)
        if isPrime(candidate):
            return candidate

def get_flag_value():
    with open("flag.txt", "rb") as f:
        return bytes_to_long(f.read().strip())

def elliptic_curve_encrypt(flag_val):
    p = getPrime(512)
    q = getPrime(512)

    modulus = p * q # ecc_modulus

    y = randint(0, modulus - 1)
    a = randint(1, modulus)
    b = (y**2 - (flag_val**3 + a * flag_val)) % modulus

    curve = EllipticCurve(Zmod(modulus), [a, b])
    base = curve(flag_val, y)
    result_point = 2 * base

    encrypted = pow(bytes_to_long(b'ANA M9WD'), 0x10001, modulus)

    return {
        "a": a,
        "b": b,
        "point": result_point.xy(),
        "modulus": modulus,
        "ciphertext": encrypted
    }

def hybrid_encrypt(flag_val, ecc_modulus):
    P = generate_custom_prime()
    Q = generate_custom_prime()
    rsa_modulus = P * Q

    pub = pow(flag_val + P, 0x10001, ecc_modulus)

    rsa_ciphertext = pow(bytes_to_long(b'ANA CHIKOUR'), 0x10001, rsa_modulus)

    return {
        "rsa_modulus": rsa_modulus,
        "pub": pub,
        "ciphertext": rsa_ciphertext
    }

def save_all(ecc_data, hybrid_data):
    with open("ecc_info.txt", "w") as f:
        f.write(f"a = {ecc_data['a']}\n")
        f.write(f"b = {ecc_data['b']}\n")
        f.write(f"point = {ecc_data['point']}\n")
        f.write(f"modulus = {ecc_data['modulus']}\n")
        f.write(f"ciphertext = {ecc_data['ciphertext']}\n")

    with open("rsa_info.txt", "w") as f:
        f.write(f"rsa_modulus = {hybrid_data['rsa_modulus']}\n")
        f.write(f"pub = {hybrid_data['pub']}\n")
        f.write(f"ciphertext = {hybrid_data['ciphertext']}\n")

def main():
    flag_val = get_flag_value()
    ecc_data = elliptic_curve_encrypt(flag_val)
    hybrid_data = hybrid_encrypt(flag_val, ecc_data["modulus"])
    save_all(ecc_data, hybrid_data)

main()
```

From this code, we observe several key vulnerabilities:

### RSA Weakness (generate_custom_prime)
- Primes P and Q for `rsa_modulus` are generated using `generate_custom_prime()`
- This function constructs a candidate prime by concatenating a random 100-bit prefix and a 140-bit suffix
- The suffix generation is the critical vulnerability: `str(getRandomNBitInteger(140)).encode().hex()[2:]`
- This converts a random number to its string representation (e.g., "123"), then encodes it to bytes (e.g., b'123'), and finally hex-encodes these bytes (e.g., b'313233')
- **Crucially**, the ASCII hex representation of digits '0' through '9' always starts with a 0x3 nibble (e.g., '0' is 0x30, '1' is 0x31, etc.)
- This means that the first nibble of every byte in the suffix's hex representation is fixed to 0x3
- The second nibble, however, can be any digit from 0 to 9

### Elliptic Curve Encryption (elliptic_curve_encrypt)
- Generates a standard RSA modulus n (512-bit primes p and q). This n will serve as the modulus for the ECC curve
- An elliptic curve `E: y² ≡ x³ + ax + b (mod n)` is defined
- A base point `base = curve(flag_val, y)` is set, implying `flag_val` is the x-coordinate of the base point
- The `result_point = 2 * base` is computed, and its (x, y) coordinates are leaked as `point`
- This implies `point[0]` is the x-coordinate of 2 * base
- The ciphertext based on b'ANA M9WD' is a distraction

### Hybrid Encryption (hybrid_encrypt)
- Uses the vulnerable `generate_custom_prime()` to get P and Q, forming `rsa_modulus = P * Q`
- Calculates `pub = pow(flag_val + P, 0x10001, ecc_modulus)`
- This is the direct link to the `flag_val` and one of the vulnerable primes P, encrypted under the ECC modulus n
- The `rsa_ciphertext` based on b'ANA CHIKOUR' is another distraction

**Goal**: Recover `flag_val`.

## Task Analysis

The challenge requires a multi-stage approach:

1. **Exploit the weak RSA prime generation**: Recover the LSBs of P and Q from `rsa_modulus` using the fixed 0x3 nibble vulnerability
2. **Factor rsa_modulus completely**: Use Coppersmith's method to find the remaining unknown MSBs of P and Q once enough LSBs are known
3. **Find flag_val**: With P (or Q) known, use the `pub` value from `hybrid_encrypt` and the `point` value from `elliptic_curve_encrypt` to form two polynomials in `flag_val`. The `flag_val` will be the common root of these polynomials

## Exploitation

### Part 1: Recovering RSA Prime LSBs

The `generate_custom_prime` function's suffix ensures that the LSBs of the primes P and Q have a peculiar structure when viewed in hexadecimal. For every byte in the suffix, the first nibble is 0x3. For example, if a random number was 12, its string representation is "12", encoded to b'12', and then hex-encoded to b'3132'. This means the prime would contain 0x31 followed by 0x32 in its LSBs.

We can exploit this by brute-forcing the second nibble of each byte. Since the original random number for the suffix is 140 bits, this corresponds to 140/4 = 35 hex characters, or approximately 35/2 ≈ 17 bytes. We can iterate from the LSB upwards, recovering two nibbles (one full byte) at a time for P and Q.

The function `bf_2nd_nibbles` does exactly this:

```python
def bf_2nd_nibbles(N, A, B, n):
    for x in range(16): # Possible values for the 2nd nibble of P
        for y in range(16): # Possible values for the 2nd nibble of Q
            # Construct candidate for P's current byte: 0x3XY... (where XY is the new byte)
            bfA = 0x3 * pow(16, n - 1) + pow(16, n - 2) * x + A
            # Construct candidate for Q's current byte: 0x3XY...
            bfB = 0x3 * pow(16, n - 1) + pow(16, n - 2) * y + B
            # Check if the product of current partial primes matches N modulo 16^n
            if bfA * bfB % pow(16, n) == N % pow(16, n):
                return bfA, bfB # Found the correct nibble pair
    return None, None

p = q = 0
for i in range(2, 86, 2): # Iterate over pairs of nibbles (bytes)
    p, q = bf_2nd_nibbles(rsa_n, p, q, i)
```

The loop `range(2, 86, 2)` attempts to recover up to 86/2 = 43 bytes of the LSBs. This covers more than the 140 bits (17.5 bytes) from the suffix, ensuring we get all of it.

### Part 2: Factoring RSA with Coppersmith's Method

After recovering the known LSBs of P and Q (let's call them `p_known` and `q_known`), we have:

```
P = High_P * 2^k + p_known
Q = High_Q * 2^k + q_known
```

where k is the number of bits known from the LSBs.

We know `N = P * Q`. Substituting the expressions:

```
N = (High_P * 2^k + p_known) * (High_Q * 2^k + q_known)
```

This is a polynomial in `High_P` and `High_Q`. Since these higher parts are relatively "small" compared to the full primes (after we've recovered a significant portion of the LSBs), we can use Coppersmith's method.

The solver uses the following setup for Coppersmith:

```python
R = 2 ** (p.bit_length()) # R represents the magnitude of the known LSB part
x, y = var('x y')
p_ = x * R + p # x is the unknown high part of P
q_ = y * R + q # y is the unknown high part of Q
f = (p_ * q_ - rsa_n).expand() # The polynomial f(x, y)

PR = PolynomialRing(Zmod(rsa_n), names=('x', 'y'))
f = PR(f)
x, y = f.parent().gens()

# Use Coppersmith's small_roots function
roots = small_roots(f, [R, R], m=3, d=4) # Search for roots up to R
x_root, y_root = roots[0]

P = int(x_root * R + p) # Reconstruct P
assert rsa_n % P == 0 # Verify P is a factor
Q = rsa_n // P # Compute Q
```

This successfully recovers the full P and Q values.

### Part 3: Recovering the Flag via Polynomial GCD

The final step is to find the `flag_val`. The challenge hides `flag_val` as a common root of two polynomials defined over **Z_n** (where n is the ECC modulus).

#### Polynomial from hybrid_encrypt
We have `pub = pow(flag_val + P, 0x10001, ecc_modulus)`. Let `z = flag_val`. Then:

```
(z + P)^0x10001 ≡ pub (mod n)
```

So, one polynomial is `f(z) = (z + P)^0x10001 - pub (mod n)`.

#### Polynomial from elliptic_curve_encrypt
We have `base = curve(flag_val, y)` and `result_point = 2 * base`. We are given `point[0]` (the x-coordinate of 2 * base).

The x-coordinate of a point `2(x₁, y₁)` on an elliptic curve `y² = x³ + ax + b` is given by the formula:

```
x₂ = ((3x₁² + a) / (2y₁))² - 2x₁
```

Let `x₁ = z = flag_val` and `x₂ = point[0]`. Then:

```
point[0] = ((3z² + a) / (2y))² - 2z
```

Rearranging and eliminating y using `y² = z³ + az + b`:

```
(2y)²(point[0] + 2z) = (3z² + a)²
4(z³ + az + b)(point[0] + 2z) = (3z² + a)²
```

So, the second polynomial is:

```
g(z) = (3z² + a)² - 4(z³ + az + b)(2z + point[0]) (mod n)
```

The `flag_val` is the common root of `f(z)` and `g(z)`. This can be found by computing their polynomial GCD.

```python
F = Zmod(n) # Modulus for ECC
PR = PolynomialRing(F, names=('z',))
z = PR.gen()

f = (z + Q) ** 0x10001 - pub
g = (3 * z**2 + a)**2 - 4 * (z**3 + a * z + b) * (2 * z + point[0])

# Compute polynomial GCD
pgcd = lambda g1, g2: g1.monic() if not g2 else pgcd(g2, g1 % g2)
m = -pgcd(f, g).coefficients()[0] # If GCD is (z - m), then constant term is -m

print(long_to_bytes(int(m)))
```

The `long_to_bytes` conversion of m reveals the flag.

## Behind the Math

### Weak Prime Suffix
The ASCII hex encoding of digits ('0'-'9') ensures that for each byte corresponding to a digit, the most significant nibble will always be 0x3. This predictable pattern drastically reduces the search space for the LSBs from 16×16 (256) possibilities per byte pair to 10×10 (100) possibilities, allowing for practical brute-force recovery.

### Coppersmith's Method
This powerful technique (specifically the theorem by Coppersmith for finding small roots of polynomials modulo N) is essential for factoring `rsa_n`. Once a significant portion of the prime factors is known (either MSBs or LSBs), the remaining unknown bits can be found efficiently by treating them as small roots of a carefully constructed polynomial equation. The efficiency comes from lattice reduction algorithms like LLL.

### Elliptic Curve Point Doubling and Polynomial Roots
The x-coordinate of 2P on an elliptic curve (`y² = x³ + ax + b`) is given by:

```
x(2P) = ((3x(P)² + a) / (2y(P)))² - 2x(P)
```

By substituting `x(P) = z` and `x(2P) = point[0]`, and using the curve equation to eliminate `y(P)`, we can derive a polynomial in z. If z is the flag, it must be a root of this polynomial.

### Polynomial GCD for Common Roots
If a value m is a root of two distinct polynomials `f(x)` and `g(x)`, then `(x - m)` must be a factor of both polynomials. This means `(x - m)` is a common divisor, and thus a factor of `gcd(f(x), g(x))`. If there's only one common root, `gcd(f(x), g(x))` will be a linear polynomial of the form `C(x - m)`, where C is a constant. By normalizing it to a monic polynomial, we get `(x - m)`, and the root m can be easily extracted from its coefficients.

## Conclusions

"Vrai Sahl" was a challenging but rewarding CTF problem that demonstrated:

- **The critical importance of truly random prime generation**: Even small, subtle patterns in prime construction can lead to complete factorization
- **The power of Coppersmith's method**: It's a fundamental tool for solving problems involving small roots of polynomials modulo large integers, often seen in RSA attacks
- **Interdisciplinary cryptography**: How vulnerabilities can arise at the intersection of different cryptographic primitives (RSA and ECC) and how their properties can be combined to extract secrets
- **Polynomial algebra in cryptanalysis**: Leveraging polynomial GCD to find unknown values that satisfy multiple equations

This challenge exemplifies a sophisticated attack path, combining various number theoretic and cryptographic concepts to demonstrate how seemingly small implementation flaws can lead to complete system compromise.
