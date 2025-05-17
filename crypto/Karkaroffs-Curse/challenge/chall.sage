from hashlib import md5
from Crypto.Util.number import long_to_bytes, getPrime
outputs = []

# Read the flag as bytes
with open('flag.txt', 'rb') as f:
    flag = f.read().rstrip()

for ingeniums in flag:
    while True:
        patron = Integer(getPrime(256))  
        quantom = Integer(getPrime(256))
        nano = patron * quantom
        freedom = (patron - 1) * (quantom - 1)
        elliptic = Integer(getPrime(13))
        try:
            diddy = inverse_mod(elliptic, freedom)  
            krypto = (elliptic * diddy - 1) //freedom 
            rust = md5(long_to_bytes(krypto)).digest() + md5(long_to_bytes(ingeniums)).digest()
            outputs.append(md5(rust).digest())
        except ZeroDivisionError:
            continue
        break

with open('output.txt', 'wb') as f:
    for o in outputs:
        f.write(o.hex().encode() + b'\n')



