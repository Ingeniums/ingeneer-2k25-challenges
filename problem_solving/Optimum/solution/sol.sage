A = matrix(QQ,[
[  1,   0,   0,   0],
[  0,  14,  -3,   0],
[  0,  52, -11,   0],
[  0,   0,   0,   1],
])
A = A
B = A.diagonalization()[1] * A.diagonalization()[0]**100000000 * A.diagonalization()[1].inverse()
# pass this to long_to_bytes
print(str(sum(B * vector([1,1,1,1])) - int(4529244483418829500472511508539901009924817085897422363305051223681352720395787375204150722130519893))[-100:])