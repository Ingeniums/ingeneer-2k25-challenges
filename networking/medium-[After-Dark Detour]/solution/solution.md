# Network Configuration Solution

## Configuration Overview
This configuration implements a time-based routing policy using route maps and access lists.

## Configuration Details

```cisco
! Define time range for specific routing behavior
time-range DANGER_TIME  
 periodic daily 21:00 to 06:00   


! Primary route map entry with time-based routing
route-map PATH permit 10  
 match ip address 101   
 set ip next-hop 192.168.1.1   
 set time-range DANGER_TIME  

! Secondary route map entry for non-time-based routing
route-map PATH permit 20  
 match ip address 101   
 set ip next-hop 172.16.20.1   
```

## Explanation
- During night hours (21:00-06:00), traffic is routed through 192.168.1.1
- Outside these hours, traffic is routed through 172.16.20.1
- All IP traffic is matched using access-list 101
