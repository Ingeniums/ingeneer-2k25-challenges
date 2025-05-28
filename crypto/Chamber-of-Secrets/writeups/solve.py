from Crypto.Util.number import long_to_bytes
from sympy import factorint
from pwn import remote

n = 110001622643652618410484939904361556508203623908752103099147453775998534938941884955333249092645022563126552010285659941596667300912600376824495403275435509828970792133204833060934823127312564724706739514055174033751863340022771906054555499136506784343792084879737434332549807807656949563244850995995342249449 
ct = 34039095913024599545562118069598224892841144417232942267162804018336214704715562324723900337288402100485673058644252241734290447812911151180243132476360162366874334575924849963740962614488393476631805693987679799878312570508401863570557684848330526744187102187091

factors = factorint(ct)
primes = []
for p, exp in factors.items():
    primes.extend([p] * exp)

signatures = []
for prime in primes:
    conn = remote('chamber-of-secrets.ingeneer.ingeniums.club', 30013)
    conn.recvuntil(b'Choose 1 or 2:')
    conn.sendline(b'1')
    conn.recvuntil(b'Enter integer M to sign:')
    conn.sendline(str(prime).encode())
    conn.recvuntil(b'Here is your signature sigma = M^d mod n:\n')
    line = conn.recvline().strip()
    sigma = int(line)
    signatures.append(sigma)
    conn.close()
M = 1
for s in signatures : 
    M *= s 
    M %= n 
conn = remote('chamber-of-secrets.ingeneer.ingeniums.club', 30013)
conn.recvuntil(b'Choose 1 or 2:')
conn.sendline(b'2')
conn.recvuntil(b'Enter the magic incantation: ')
conn.sendline(str(M).encode())
print(conn.recvlines(3)[-1])


