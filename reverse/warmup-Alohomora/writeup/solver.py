import os

filename = 'flag.txt.enc'

def srand(seed):
    global current_seed
    current_seed = seed - 4

def rand():
    global current_seed
    current_seed = (0x5A51F42A4C957F2A * current_seed + 1) & 0xFFFFFFFFFFFFFFFF
    return current_seed >> 33

mod_time = int(os.path.getmtime(filename))
srand(mod_time)

f = open(filename, 'rb')
content = f.read()

flag = bytearray()
for byte in content:
    flag.append(byte ^ (rand() % 127))

print(f'Flag: {"".join(map(chr, flag))}') 