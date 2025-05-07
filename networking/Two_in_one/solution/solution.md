📁 **PC2:**  
Inside the `notebook`, you’ll find a file named `super secret.txt` with the following content:

```
the key:  2590723872081184218917971932865193458325535145631397698209772701303205879762222217148938434749909075735278340077200962114606902325289703602347294071578808408284039031567827802401513958922481022854828163270506318591148513780420390818298188986090183041755858102216723043004868324800859303415371473130034628409
```

This is the **ciphertext of the flag**, which has been encrypted using RSA.

---

📁 **PC3:**  
You will also find a file named `not that secret:).txt` containing:

```
TXpJME5qYzVOalUyTXprNU5EQXpNekF4TnpZek9UZzFOakl4TmpRM056TXpOekEwTXprNE5URTNNakF5T0RrM05UVTJNRGc1TlRnNU5EQXdOVFl4T0Rnek5UQXpPREl4T1RVMk9EVTFNVFkyT0RBMk16WTNOamcxTkRNek5UUTFPVGt5T0RNNE56RTVPREU0TkRJNU56WTBNakE1TnpFMk5EUXhNVFE0TmpJd05EWXhPVGMxTmpRNE1qTXlOamN5TXpNNE9UWTBOell5T0RFMU9EZzRNakExTmpjeU56VXlNelUzT0RjNU9ETTNOVFk1TURBeU16Y3hOVGd3TXpFek56VTJNVEkzT0RNNE1EQXdORGMwT1RNeU16azNOVFV6T0RFMk9EZzBNelEyTURJMU5EUXlOall3TnpnNE1UYzVNVGMzTmpZd01USTVNRFUyTlRZM016QTFNRFkyTmpRNE1UQTJNREU0TlRjMk1UazRNVE00TkRjek5URXhNamd3TWpJek1UWTVORFF3TlRNek16UXlOakE0Tnc9PQ==
```

🔎 Decode this **base64 string twice**, and you'll get a number — this is your **RSA modulus `n`**.

---

### 🔐 Encryption Details

- `e = 65537`
- `n` (decoded from above) is vulnerable to **Fermat's factorization**
- Use the following Python script to **decrypt the ciphertext** and retrieve the flag:

```python
from math import isqrt
from Crypto.Util.number import inverse

# RSA modulus from decoded base64
n = 3246796563994033017639856216477337043985172028975560895894005618835038219568551668063676854335459928387198184297642097164411486204619756482326723389647628158882056727523578798375690023715803137561278380004749323975538168843460254426607881791776601290565673050666481060185761981384735112802231694405333426087

# Fermat's factorization
def fermat_factor(n):
    a = isqrt(n)
    if a * a < n:
        a += 1
    b2 = a * a - n
    count = 0
    while not isqrt(b2)**2 == b2:
        a += 1
        b2 = a * a - n
        count += 1
    b = isqrt(b2)
    return a - b, a + b, count

# Factor n
p, q, steps = fermat_factor(n)
assert p * q == n

# Public key
e = 65537

# Ciphertext (from super secret.txt)
c = 2590723872081184218917971932865193458325535145631397698209772701303205879762222217148938434749909075735278340077200962114606902325289703602347294071578808408284039031567827802401513958922481022854828163270506318591148513780420390818298188986090183041755858102216723043004868324800859303415371473130034628409

# Compute private key
phi = (p - 1) * (q - 1)
d = inverse(e, phi)

# RSA decryption
def rsa_decrypt(ciphertext_int, d, n):
    m = pow(ciphertext_int, d, n)
    plaintext_bytes = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')
    return plaintext_bytes.decode()

# Decrypt and print the flag
flag = rsa_decrypt(c, d, n)

print("🔓 Decrypted Flag:", flag)
```

---

### 🏁 Flag

```
1ng3neer2k25{Crypt0_plus_N3tw0rk1ng_3qual5_fr13nd5}
```

