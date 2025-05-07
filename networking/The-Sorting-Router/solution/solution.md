# Hogwarts Network: The Sorting Hat's Vulnerability

## Magical Network Overview
The enchanted Sorting Hat assigns **houses (IP addresses)** to first-year devices (DHCP clients) across Hogwarts' network. However, its configuration lacks critical security enchantments—most notably, **DHCP Snooping** protections.

## The Dark Arts Threat
A **DHCP Starvation** attack plagues the castle's network:
- Death Eaters flood the Sorting Hat with false requests  
- The Hat's magic (DHCP pool) is exhausted  
- New devices remain **houseless** (unable to obtain IPs)  

## Challenge Objective
Discover and demonstrate this attack to help Professor Flitwick secure the network. The flag follows the format:  
`1ng3neer2k25{dhcp_starvation}`

> *"When endless requests the Hat doth bear,  
> Its magic fades—beware, beware!"*  