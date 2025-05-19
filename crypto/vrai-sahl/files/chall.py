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
    modulus = p * q

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

