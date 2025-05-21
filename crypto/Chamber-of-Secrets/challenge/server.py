#!/usr/bin/env python3
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from secrets import m

with open('sk.pem', 'rb') as f:
    sk = RSA.import_key(f.read())
e = 0x10001
n = sk.n

def sign(sk, M):
    mp, dq = M % sk.q, sk.d % (sk.q - 1)
    mq, dp = M % sk.p, sk.d % (sk.p - 1)
    s1 = pow(mq, dq, sk.q)
    s2 = pow(mp, dp, sk.p)
    h = (sk.u * (s1 - s2)) % sk.q
    return (s2 + h * sk.p) % sk.n

def main():
    print("Welcome to the Hogwarts Signature Challenge")
    print("The Chamber of Cryptic Runes Awaits")
    print()
    print("Grand Modulus (n):", n)
    ct = pow(m, e, n)
    print("Invisibility Cipher (ct = m^e mod n):", ct)
    print()
    print("1) Sign a number")
    print("2) Offer the magic incantation to win the prize")
    print()
    choice = input("Choose 1 or 2: ").strip()
    if choice == '1':
        raw = input("Enter integer M to sign: ").strip()
        if not raw or not raw.lstrip('-').isdigit():
            print("Invalid input. Exiting.")
            return
        M = int(raw)
        sig = sign(sk, M)
        print("Here is your signature sigma = M^d mod n:")
        print(sig)
        print("Mischief Managed!")
    elif choice == '2':
        raw = input("Enter the magic incantation: ").strip()
        if not raw or not raw.lstrip('-').isdigit():
            print("Invalid input. Exiting.")
            return
        guess = int(raw)
        if guess == m:
            try:
                flag = open('flag.txt').read().strip()
            except:
                flag = "[error reading flag]"
            print("Congratulations! The magic is true.")
            print("Here is your prize:")
            print(flag)
        else:
            print("That is not the correct magic incantation.")
        print("Mischief Managed!")
    else:
        print("Invalid choice. Exiting.")

if __name__ == '__main__':
    main()
