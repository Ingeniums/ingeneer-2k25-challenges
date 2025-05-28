from Crypto.Util.number import *
from sage.all import *

load('coppersmith.sage')

def read_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
    return dict(line.strip().split(" = ", 1) for line in lines)

def parse_point(point_str):
    x_str, y_str = point_str.strip("()").split(",")
    return int(x_str), int(y_str)

ecc = read_file("ecc_info.txt")
rsa = read_file("rsa_info.txt")

a = int(ecc["a"])
b = int(ecc["b"])
point = parse_point(ecc["point"])
n = int(ecc["modulus"])
ciphertext_ecc = int(ecc["ciphertext"])

rsa_n = int(rsa["rsa_modulus"])
pub = int(rsa["pub"])
ciphertext_rsa = int(rsa["ciphertext"])

def bf_2nd_nibbles(N, A, B, n):
    for x in range(16):
        for y in range(16):
            bfA = 0x3 * pow(16, n - 1) + pow(16, n - 2) * x + A
            bfB = 0x3 * pow(16, n - 1) + pow(16, n - 2) * y + B
            if bfA * bfB % pow(16, n) == N % pow(16, n):
                return bfA, bfB
    return None, None

p = q = 0
for i in range(2, 86, 2):
    p, q = bf_2nd_nibbles(rsa_n, p, q, i)

R = 2 ** (p.bit_length())

x, y = var('x y')
p_ = x * R + p
q_ = y * R + q
f = (p_ * q_ - rsa_n).expand()

PR = PolynomialRing(Zmod(rsa_n), names=('x', 'y'))
f = PR(f)
x, y = f.parent().gens()

roots = small_roots(f, [R, R], m=3, d=4)
x_root, y_root = roots[0]

P = int(x_root * R + p)
assert rsa_n % P == 0
Q = rsa_n // P

F = Zmod(n)
PR = PolynomialRing(F, names=('z',))
z = PR.gen()

f = (z + Q) ** 0x10001 - pub
g = (3 * z**2 + a)**2 - 4 * (z**3 + a * z + b) * (2 * z + point[0])

pgcd = lambda g1, g2: g1.monic() if not g2 else pgcd(g2, g1 % g2)
m = -pgcd(f, g).coefficients()[0]

print(long_to_bytes(int(m)))



