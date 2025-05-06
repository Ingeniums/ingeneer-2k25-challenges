
from secrets import choice
from Crypto.Util.number import bytes_to_long, getPrime

charset = "abcdefghijklmnopqrstuvwxyz0123456789"
m = ''.join(choice(charset) for _ in range(33)) + '0000'
m_int = bytes_to_long(m.encode())

p = getPrime(256)
r = m_int % p

assert 1099511627776 * p > m_int

print(f"p: {p}")
print(f"r: {r}")

while True:
    try:
        user_input = input("enter m: ")
        if not user_input.strip():
            break
        user_m = int(user_input.strip())
        if user_m == m_int:
            flag = open("flag.txt").read()
            print(flag, end='')  
            break
        else:
            print("Wrong answer! Try again.")
    except ValueError:
        print("Invalid input! Try again.")
    except Exception:
        print("Invalid input or error occurred!")
        break
