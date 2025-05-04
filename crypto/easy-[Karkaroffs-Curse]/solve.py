from hashlib import md5
from Crypto.Util.number import long_to_bytes
from string import printable
output = []

with open('output.txt', 'r') as f:
    for line in f:
        output.append(bytes.fromhex(line.rstrip()))

for i in output : 
    for k in range(2**13) :
        for p in printable :
                r = md5(long_to_bytes(k)).digest() + md5(long_to_bytes(ord(p))).digest()
                if i ==md5(r).digest():
                    print(p)
