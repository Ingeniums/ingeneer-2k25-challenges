from Crypto.Util.number import *
from secret import flag 
from math import gcd

e1, e2 = 40229, 30387
assert len(flag) == 40

while True:
    p, q = getPrime(1024), getPrime(1024)
    phi = (p - 1) * (q - 1)

    if gcd(e1, phi) == 1 and gcd(e2, phi) == 1:
        n = p * q
        m = bytes_to_long(flag)
        c1 = pow(m, e1, n)
        c2 = pow(m, e2, n)
        break

with open("output.txt", "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"c1 = {c1}\n")
    f.write(f"c2 = {c2}\n")

