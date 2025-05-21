from pwn import *

p = remote('localhost', 12376)

# for a1 to a4
p.recvuntil(': \n')
p.sendline('0.50')
p.recvuntil(': \n')
p.sendline('1.20')
p.recvuntil(': \n')
p.sendline('4.36')
p.recvuntil(': \n')
p.sendline('3.75')

# # for a1 to a4
# p.recvuntil(': \n')
# p.sendline('9.20')
# p.recvuntil(': \n')
# p.sendline('0.50')
# p.recvuntil(': \n')
# p.sendline('4.36')
# p.recvuntil(': \n')
# p.sendline('3.75')

# for b1 to b4
p.recvuntil(': \n')
p.sendline('0.75')
p.recvuntil(': \n')
p.sendline('1.92')
p.recvuntil(': \n')
p.sendline('6.005651863464892')
p.recvuntil(': \n')
p.sendline('1.1343481365351082')

# for c1 to c4
p.recvuntil(': \n')
p.sendline('1.00')
p.recvuntil(': \n')
p.sendline('3.60')
p.recvuntil(': \n')
p.sendline('4.620198501388883')
p.recvuntil(': \n')
p.sendline('0.589801498611117')

# for d1 to d4
p.recvuntil(': \n')
p.sendline('2.50')
p.recvuntil(': \n')
p.sendline('0.96')
p.recvuntil(': \n')
p.sendline('5.623085987051925')
p.recvuntil(': \n')
p.sendline('0.7269140129480747')

# finally, print the flag
print(p.recvall().decode())

