from Crypto.Util.number import getPrime, bytes_to_long
from sage.all import *
from random import getrandbits
from flag import SECRET

S = bytes_to_long(SECRET)
rock = getrandbits(30)

roots = [getPrime(19) for _ in range(19)]
branches = [getPrime(19) for _ in range(19)]

Quidditch = 99999999999999999999999999999999999999999999

forest_whisper = sum(S*(roots[i]**2) + rock*(branches[i]**2)*Quidditch for i in range(19))


F = RDF 
x = vector(F, roots)
y = vector(F, branches)
b = round(y.norm()**2)
for _ in range(119):
    A = random_matrix(F, 19)
    Q, R = A.QR()
    x = Q * x
    y = Q * y

with open("x_vector.txt", "w") as f_x:
    for value in x:
        f_x.write(f"{value}\n")

with open("y_vector.txt", "w") as f_y:
    for value in y:
        f_y.write(f"{value}\n")

with open("whisper.txt","w") as f :
    f.write(str(forest_whisper))



