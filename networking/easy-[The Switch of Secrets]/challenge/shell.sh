#!/bin/bash
# challenge.sh: Interactive challenge script

# Function to display the environment options
show_menu() {
  clear
  echo "Welcome to the magical network challenge!"
  echo "Please choose an environment to enter:"
  echo "  1: Hogwarts-Castle (Router)"
  echo "  2: Gryffindor-Common-Room (Switch 1)"
  echo "  3: Slytherin-Dungeon (Switch 2)"
  echo -n "Enter your choice (1-3, or 'q' to quit): "
}

# Function to simulate the router environment
router_env() {
  echo "You are now in Hogwarts-Castle (Router). Type 'exit' to return to menu."
  echo "Allowed commands: show ip interface brief, show interfaces description, show version"
  echo "Type your command:"
  while read -r cmd; do
    case "$cmd" in
      "exit")
        return
        ;;
      "show ip interface brief")
        cat <<EOF
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.168.1.1     YES NVRAM  up                    up
GigabitEthernet0/1     192.168.2.1     YES NVRAM  up                    up
Vlan1                  unassigned      YES unset  administratively down down
EOF
        ;;
      "show interfaces description")
        cat <<EOF
GigabitEthernet0/0 is up, line protocol is up (connected)
  Description: Keep this secret hidden like a well-guarded Horcrux
  Internet address is 192.168.1.1/24
GigabitEthernet0/1 is up, line protocol is up (connected)
  Description: Spread it and it may fly FASTer than a Firebolt!
  Internet address is 192.168.2.1/24
Vlan1 is administratively down, line protocol is down
EOF
        ;;
      "show version")
        cat <<EOF
Cisco IOS Software, C2900 Software (C2900-UNIVERSALK9-M), Version 15.1(4)M4, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2012 by Cisco Systems, Inc.
Compiled Thurs 5-Jan-12 15:41 by pt_team
EOF
        ;;
      *)
        echo "Please type an allowed command or 'exit' to return to menu."
        ;;
    esac
    echo -n "Router> "
  done
}

# Function to simulate the first switch environment (Gryffindor-Common-Room)
switch1_env() {
  echo "You are now in Gryffindor-Common-Room (Switch 1). Type 'exit' to return to menu."
  echo "Allowed commands: show ip interface brief, show interfaces description"
  echo "Type your command:"
  while read -r cmd; do
    case "$cmd" in
      "exit")
        return
        ;;
      "show ip interface brief")
        cat <<EOF
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/2        unassigned      YES NVRAM  up                    up
FastEthernet0/3        unassigned      YES NVRAM  down                  down
FastEthernet0/4        unassigned      YES NVRAM  down                  down
FastEthernet0/5        unassigned      YES NVRAM  down                  down
FastEthernet0/6        unassigned      YES NVRAM  down                  down
FastEthernet0/7        unassigned      YES NVRAM  down                  down
FastEthernet0/8        unassigned      YES NVRAM  down                  down
FastEthernet0/9        unassigned      YES NVRAM  down                  down
FastEthernet0/10       unassigned      YES NVRAM  down                  down
FastEthernet0/11       unassigned      YES NVRAM  down                  down
FastEthernet0/12       unassigned      YES NVRAM  down                  down
GigabitEthernet0/1     unassigned      YES NVRAM  up                    up
Vlan1                  unassigned      YES unset  administratively down down
EOF
        ;;
      "show interfaces description")
        cat <<EOF
FastEthernet0/1:
FastEthernet0/2:
FastEthernet0/3:
FastEthernet0/4:
FastEthernet0/5:
FastEthernet0/6:
FastEthernet0/7:  1ng3neer2k25{magic_wand_spell}
FastEthernet0/8:
FastEthernet0/9:
FastEthernet0/10:
FastEthernet0/11:
FastEthernet0/12:
EOF
        ;;
      *)
        echo "Please type an allowed command or 'exit' to return to menu."
        ;;
    esac
    echo -n "Switch1> "
  done
}

# Function to simulate the second switch environment (Slytherin-Dungeon)
switch2_env() {
  echo "You are now in Slytherin-Dungeon (Switch 2). Type 'exit' to return to menu."
  echo "Allowed commands: show ip interface brief, show interfaces description, show version"
  echo "Type your command:"
  while read -r cmd; do
    case "$cmd" in
      "exit")
        return
        ;;
      "show ip interface brief")
        cat <<EOF
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/1        unassigned      YES NVRAM  up                    up
FastEthernet0/2        unassigned      YES NVRAM  up                    up
FastEthernet0/3        unassigned      YES NVRAM  down                  down
FastEthernet0/4        unassigned      YES NVRAM  down                  down
FastEthernet0/5        unassigned      YES NVRAM  down                  down
FastEthernet0/6        unassigned      YES NVRAM  down                  down
FastEthernet0/7        unassigned      YES NVRAM  down                  down
FastEthernet0/8        unassigned      YES NVRAM  down                  down
FastEthernet0/9        unassigned      YES NVRAM  down                  down
FastEthernet0/10       unassigned      YES NVRAM  down                  down
FastEthernet0/11       unassigned      YES NVRAM  down                  down
FastEthernet0/12       unassigned      YES NVRAM  down                  down
GigabitEthernet0/1     unassigned      YES NVRAM  up                    up
Vlan1                  unassigned      YES unset  administratively down down
EOF
        ;;
      "show interfaces description")
        cat <<EOF
FastEthernet0/1:
FastEthernet0/2:
FastEthernet0/3:
FastEthernet0/4:
FastEthernet0/5:
FastEthernet0/6:
FastEthernet0/7:  
FastEthernet0/8:
FastEthernet0/9:
FastEthernet0/10:
FastEthernet0/11:
FastEthernet0/12:
EOF
        ;;
      "show version")
        cat <<EOF
Cisco IOS Software, C3560 Software (C3560-ADVIPSERVICESK9-M), Version 12.2(37)SE1, RELEASE SOFTWARE (fc1)
Compiled Thu 05-Jul-07 22:22 by pt_team
...
EOF
        ;;
      *)
        echo "Please type an allowed command or 'exit' to return to menu."
        ;;
    esac
    echo -n "Switch2> "
  done
}

# Main loop
while true; do
  show_menu
  read -r choice
  
  case "$choice" in
    1)
      router_env
      ;;
    2)
      switch1_env
      ;;
    3)
      switch2_env
      ;;
    q|Q)
      echo "Goodbye!"
      exit 0
      ;;
    *)
      echo "Invalid choice. Please enter 1, 2, or 3."
      sleep 1
      ;;
  esac
done