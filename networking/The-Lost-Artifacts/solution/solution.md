There are some missing commands you need to complete

In the switch ElderWandSwitch we need

```
interface gigabitEthernet 0/1
switchport mode trunk
```

In the switch InvisibilityCloakSwitch we need

```
interface fastEthernet 0/2
switchport mode access
```

In the router GryffindorRouter we need:

```
ip route 50.0.0.0 255.255.255.0 30.0.0.2
ip route 70.0.0.0 255.255.255.0 30.0.0.2
```

In the router HufflepuffRouter we need:

```
ip route 20.0.0.0 255.255.255.0 30.0.0.1
```
In the router RavenclawRouter we need:

```
ip route 10.0.0.0 255.255.255.0 40.0.0.1
ip route 60.0.0.0 255.255.255.0 50.0.0.2
```
In the router SlytherinRouter we need:

```
ip route 30.0.0.0 255.255.255.0 50.0.0.1
```
