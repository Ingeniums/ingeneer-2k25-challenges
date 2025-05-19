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

ecc_data = read_file("ecc_output.txt")
rsa_dh_data = read_file("rsa_dh_output.txt")

a = int(ecc_data["a"])
b = int(ecc_data["b"])
point = parse_point(ecc_data["point"])
n = int(ecc_data["n"])
ciphertext_ecc = int(ecc_data["ciphertext"])

N = int(rsa_dh_data["N"])
G = int(rsa_dh_data["G"])
ciphertext_rsa = int(rsa_dh_data["C"])

def bf_2nd_nibbles(N, A, B, n):
    for x in range(16):
        for y in range(16):
            bfA = 0x3 * pow(16, n - 1) + pow(16, n - 2)*x + A
            bfB = 0x3 * pow(16, n - 1) + pow(16, n - 2)*y + B
            if bfA * bfB % pow(16, n) == N % pow(16, n):
                return bfA, bfB
p = q = 0
for i in range(2, 86, 2):
    p, q = bf_2nd_nibbles(N, p, q, i)
R = 2**(p.bit_length())
x, y = var('x y')
p_ = x * R + p
q_ = y * R + q
f = (p_ * q_ - N).expand()
PR = PolynomialRing(Zmod(N), names=('x', 'y'))
f = PR(f)
x, y = small_roots(f, [R, R], m=3, d=4)[0]

P = x * R + p
P = int(P)
assert N % P  == 0
Q = N // P
pgcd = lambda g1, g2: g1.monic() if not g2 else pgcd(g2, g1%g2)
F = Zmod(n)

PR = PolynomialRing(Zmod(n), names=('z',))

z = PR.gen()

f = (z+Q) ** 0x10001 - G

g = (3*z**2 + a)**2 - 4*(z**3 + a*z + b)*(2*z + point[0])


m = -pgcd(f, g).coefficients()[0]

print(int(m))



