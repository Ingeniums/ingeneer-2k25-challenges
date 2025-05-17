#!/usr/bin/env python3

def main():
    print("Network Configuration Terminal")
    print("Enter network commands. Type 'exit' to quit.")
    
    correct_command = "ip route add 192.168.1.12/32 via 192.168.1.1"
    flag = "1ng3neer2k25{r0ut3rs_sh0uldnt_b3_th1t_h3lpful}"
    
    while True:
        try:
            user_input = input("> ")
            
            if user_input.lower() == "exit":
                print("Exiting terminal...")
                break
            
            if user_input == correct_command:
                print("\n🎉 Correct command entered! 🎉")
                print(f"Flag: {flag}")
                print("\nCongratulations! You've successfully bypassed the PVLAN restrictions.")
                break
            else:
                print("Command executed. No output.")
                
        except KeyboardInterrupt:
            print("\nExiting terminal...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()