You have the hash of the **enable password** for the **Multi-Layer Switch**.  

Crack the password, which is **SHA-256 hashed**, using a tool like **John the Ripper** or **Hashcat**.  

Use the most famous wordlist: **rockyou.txt**.  

You will find the password:  
```
NIMBUS2000
```

Now, access the **Multi-Layer Switch**.  

You won’t see anything in the **running configuration** because the flag is stored in the **vlan.dat** file.  

Type:  
```bash
show vlan brief
```
You will find the flag in **VLAN 300's name**.  

