# Challenge Solution: The Switch of Secrets

Follow these steps to uncover the hidden flag:


1. **Inspect Router Interfaces:**
   - Once logged in, execute:
     ```
     show interfaces description
     ```
   - Look for the interface descriptions:
     - **GigabitEthernet0/0:** Should display the hint:  
       *"Keep this secret hidden like a well-guarded Horcrux"*
     - **GigabitEthernet0/1:** Should display the hint:  
       *"spread it and it may fly faster than a Firebolt!"*

2. **Check the Switch:**
   - Next, access the switch and run:
     ```
     show interfaces description
     ```
   - Identify the interface labeled as a **fast interface**. This is your key target.

3. **Find the Flag:**
   - The fast interface will have its description containing the flag.
   - Extract the flag from the description. In this challenge, the flag is:  
     `1ng3neer2k25{magic_wand_spell}`

By following these steps, you reveal the hidden secret tucked away in the fast interface of the switch. Happy hunting!
