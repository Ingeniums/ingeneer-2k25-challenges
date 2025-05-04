from Crypto.Util.number import long_to_bytes
from sage.all import *

with open("x_vector.txt", "r") as f_x:
    x_read = [float(line.strip()) for line in f_x]

with open("y_vector.txt", "r") as f_y:
    y_read = [float(line.strip()) for line in f_y]
with open("whisper.txt" , "r") as f :
    whisper = int(f.read())
F = RealField(1919)
x = vector(F, x_read)
y = vector(F, y_read)

a = round(x.norm()**2)
b = round(y.norm()**2)

S = (whisper - 19*b)//a

print(long_to_bytes(S))
