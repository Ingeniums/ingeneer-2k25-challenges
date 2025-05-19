from Crypto.Util.number import *
from random import *
from sage.all import *

def get_custom_prime():
    while True:
        sikurite = str(getRandomNBitInteger(140)).encode().hex()[2:]
        m3lomatiya= hex(getRandomNBitInteger(100))[2:]
        combined = m3lomatiya + sikurite
        candidate = int(combined, 16)
        if isPrime(candidate):
            return candidate

def load_flag():
    with open("flag.txt", "rb") as f:
        return bytes_to_long(f.read().strip())

def elliptic_curve_setup(flag_integer):
    prime_p = getPrime(512)
    prime_q = getPrime(512)
    modulus_n = prime_p * prime_q

    y_coord = randint(0, modulus_n - 1)
    curve_a = randint(1, modulus_n)
    curve_b = (y_coord**2 - (flag_integer**3 + curve_a * flag_integer)) % modulus_n

    curve = EllipticCurve(Zmod(modulus_n), [curve_a, curve_b])
    base_point = curve(flag_integer, y_coord)
    double_point = 2 * base_point

    encrypted_message = pow(bytes_to_long(b'ANA M9WD'), 0x10001, modulus_n)

    return {
        "a": curve_a,
        "b": curve_b,
        "point": double_point.xy(),
        "n": modulus_n,
        "ciphertext": encrypted_message
    }

def rsa_dh_setup(flag_integer, ecc_modulus_n):
    prime_P = get_custom_prime()

    prime_Q = get_custom_prime()
    rsa_modulus_N = prime_P * prime_Q

    base_g = 2
    dh_public_key = pow(flag_integer+prime_P, 0x10001, ecc_modulus_n)

    rsa_encrypted = pow(bytes_to_long(b'ANA CHIKOUR'), 0x10001, rsa_modulus_N)

    return {
        "N": rsa_modulus_N,
        "G": dh_public_key,
        "C": rsa_encrypted
    }

def save_results(ecc_data, rsa_dh_data):
    with open("ecc_output.txt", "w") as f:
        f.write(f"a = {ecc_data['a']}\n")
        f.write(f"b = {ecc_data['b']}\n")
        f.write(f"point = {ecc_data['point']}\n")
        f.write(f"n = {ecc_data['n']}\n")
        f.write(f"ciphertext = {ecc_data['ciphertext']}\n")

    with open("rsa_dh_output.txt", "w") as f:
        f.write(f"N = {rsa_dh_data['N']}\n")
        f.write(f"G = {rsa_dh_data['G']}\n")
        f.write(f"C = {rsa_dh_data['C']}\n")

def main():
    flag_integer = load_flag()
    ecc_data = elliptic_curve_setup(flag_integer)
    rsa_dh_data = rsa_dh_setup(flag_integer, ecc_data["n"])
    save_results(ecc_data, rsa_dh_data)

main()
