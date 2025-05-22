from Crypto.Util.number import long_to_bytes

def f(a,b,c,d,n):
    if n == 1:
        return a+14*b-3*c+52*b-11*c+d - 45292444834188295004725115085399010099248170858974223633050512236813527203957873752041507221.30519893
    elif n==0: 
        return a+b+c+d
    else:
        return f(a,14*b-3*c,52*b-11*c,d,n-1) - 45292444834188295004725115085399010099248170858974223633050512236813527203957873752041507221.30519893

# turning the result to str
flag = long_to_bytes(int(str(int(f(1,1,1,1,100000000)))[-100:]))

print(flag)


   
    

