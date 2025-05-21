from Crypto.Util.number import bytes_to_long, getPrime
from FLAG import flag  
def main():
    try:
        print("Choose an option:")
        print("option 1 : 256 bit security (very weak)")
        print("option 2 : 512 bit security (weak)")
        print("option 3 : 1024 bit security (medium)")
        print("option 4 : 2048 P-R-I-M-E M-O-D (high security)")
        option = input("Your choice: ").strip()

        if option == '4':
            n = getPrime(2048)
        elif option in ['1', '2', '3']:
            bit = int(option) * 256
            p = getPrime(bit)
            q = getPrime(bit)
            n = p * q
        else:
            print("Invalid option! Exiting.")
            return

        m = bytes_to_long(flag)
        e = 0x10001
        c = pow(m, e, n)

        print(f"n: {n}")
        print(f"e: {e}")
        print(f"c: {c}")
    
    except Exception as e:
        print("Something went wrong during setup!")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

