from Crypto.Util.number import long_to_bytes

def f(a,b,c,d,n):
    if n == 1:
        return a+14*b-3*c+52*b-11*c+d - 4529244483418829500472511508539901009924817085897422363305051223681352720395787375204150722130519.893
    elif n==0: 
        return a+b+c+d
    else:
        return f(a,14*b-3*c,52*b-11*c,d,n-1) - 4529244483418829500472511508539901009924817085897422363305051223681352720395787375204150722130519.893

# turning the result to str
flag = long_to_bytes(int(str(int(f(1,1,1,1,100000000)))[-100:]))

print(flag)


   
    

