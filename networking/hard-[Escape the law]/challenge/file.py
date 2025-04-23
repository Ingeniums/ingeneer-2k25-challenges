def normalize(command):
    """Normalize a command string for comparison."""
    return ' '.join(command.strip().lower().split())

def simulate_cli():
    """Simulates CLI configuration for two switches and checks VLAN setups in real-time."""

    accessone = False
    accesstwo = False
    trunkone = False
    trunktwo = False

    expected_sequences = {
        "1": {
            "access": ["interface f0/1", "switchport mode access", "switchport access vlan 10"],
            "trunk": ["interface f0/1", " switchport mode trunk", "switchport trunk native vlan 10"],
        },
        "2": {
            "access": ["interface f0/1", "switchport mode access", "switchport access vlan 20"],
            "trunk": ["interface f0/1", "switchport mode trunk", "switchport trunk native vlan 20"],
        }
    }

    print("Welcome to the CLI simulator!\n")

    while True:
        print("\nChoose a switch (1 or 2), or type 'exit' to quit:")
        switch_choice = input("> ").strip()

        if switch_choice.lower() == 'exit':
            break
        if switch_choice not in ["1", "2"]:
            print("Invalid choice. Please enter 1, 2, or 'exit'.")
            continue

        print(f"You are now configuring on Switch {switch_choice}. Type 'exit' to stop configuring this switch.")
        history = []
        while True:
            command = input("> ").strip()
            if command.lower() == 'exit':
                break

            normalized = normalize(command)
            history.append(normalized)

            # Check Access Mode
            expected_access = expected_sequences[switch_choice]["access"]
            idx = 0
            for cmd in history:
                if cmd == expected_access[idx]:
                    idx += 1
                    if idx == len(expected_access):
                        if switch_choice == "1":
                            if not accessone:
                                accessone = True
                                print("Access configuration successful!")
                        else:
                            if not accesstwo:
                                accesstwo = True
                                print("Access configuration successful!")
                        break

            # Check Trunk Mode
            expected_trunk = expected_sequences[switch_choice]["trunk"]
            idx = 0
            for cmd in history:
                if cmd == expected_trunk[idx]:
                    idx += 1
                    if idx == len(expected_trunk):
                        if switch_choice == "1":
                            if not trunkone:
                                trunkone = True
                                print("Trunk configuration successful!")
                        else:
                            if not trunktwo:
                                trunktwo = True
                                print("Trunk configuration successful!")
                        break

        # Flag check
        if (accessone and accesstwo) or (trunkone and trunktwo):
            print("1ng3neer2k25{1ts_all_ab0ut_t1gging}")
            break

if __name__ == "__main__":
    simulate_cli()
