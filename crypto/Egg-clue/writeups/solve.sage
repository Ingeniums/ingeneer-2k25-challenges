from Crypto.Util.number import *
from sage.all import *

with open("output.txt", "r") as f:
    lines = f.readlines()
    n = int(lines[0].split('=')[1].strip())
    c1 = int(lines[1].split('=')[1].strip())
    c2 = int(lines[2].split('=')[1].strip())

def egcd(a, b):
    if (a == 0):return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
e1, e2 = 40229, 30387

d , a , b =egcd(e1,e2)

i = inverse(c2,n)

mx = pow(c1,a,n)
my = pow(i,-b,n)

m7 = mx*my % n
print(m7)
P.<x> = PolynomialRing(Zmod(n))
b = bytes_to_long(b'1ng3neer2k25{')

l = 27*8

print(b)
a = pow(2,l)*b 

print(a)
f = (a+x)^7 - m7


print(long_to_bytes(a+int(f.small_roots(epsilon=1/30)[0])))




