First method:


In switch one: 
```
interface f0/1
switchport mode access
switchport access vlan 10

```
In the second switch:

```
interface f0/1
switchport mode access
switchport access vlan 20

```


Second method:


In switch one: 
```
interface f0/1
switchport trunk native vlan 10

```
In the second switch:

```
interface f0/1
switchport trunk native vlan 20

```


