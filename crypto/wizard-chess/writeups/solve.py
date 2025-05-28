from pwn import *
from sympy.ntheory.modular import crt 
from Crypto.Util.number import long_to_bytes,bytes_to_long
conn = remote('wizard-chess.ingeneer.ingeniums.club',30007)

p = int(conn.recvline().decode().rstrip().split(': ')[1])
r = int(conn.recvline().decode().rstrip().split(': ')[1])
mod = 1099511627776
charset = "abcdefghijklmnopqrstuvwxyz0123456789"
M = []

for c in charset : 
    rest = bytes_to_long(c.encode() + b'0000')

    m = crt([p,mod],[r,rest])[0]
    M.append(int(m))

for m in M :
    conn.sendlineafter(b'enter m: ',str(m).encode())
    print(conn.recvline())

