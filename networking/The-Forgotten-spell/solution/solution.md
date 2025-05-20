Now, access the **Multi-Layer Switch**.  

You won’t see anything in the **running configuration** because the flag is stored in the **vlan.dat** file.  

Type:  
```bash
show vlan brief
```
You will find the string in **VLAN 999's name**.  

This string is  the base64 version of the **flag** , you found it in the **Vlan database**.

Decode it twice and you will find the flag. 