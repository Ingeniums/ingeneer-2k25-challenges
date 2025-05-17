#!/bin/bash

# # Configuration flags
# check_requirements() {
#   if ! command -v bash &> /dev/null; then
#     echo "Error: bash is required but not installed."
#     exit 1
#   fi
# }

# show_header() {
#   clear
#   echo "🧙‍♂️ Welcome to the Hogwarts Network Configuration Menu"
#   echo "-----------------------------------------------------"
#   echo "Choose a device to configure:"
#   echo
# }

# show_menu() {
#   show_header
#   echo "1) GryffindorRouter"
#   echo "2) HufflepuffRouter"
#   echo "3) RavenclawRouter"
#   echo "4) SlytherinRouter"
#   echo "5) ElderWandSwitch"
#   echo "6) InvisibilityCloakSwitch"
#   echo "7) Exit"
#   echo
# }

# gryffindor_router() {
#   local has_route_50=false has_route_70=false
#    echo "✨ You chose GryffindorRouter"
#   echo "Enter configuration commands below"
#   echo "(type 'back' to return to menu, 'exit' to quit the script)"

#   while true; do
#     read -p "GryffindorRouter# " input
#     case $input in
#       exit)
#         echo "👋 Exiting script. See you at Hogwarts!"
#         exit 0
#         ;;
#       back)
#         break
#         ;;
#       "ip route 50.0.0.0 255.255.255.0 30.0.0.2")
#         echo "✅ Route to 50.0.0.0 added"
#         has_route_50=true
#         ;;
#       "ip route 70.0.0.0 255.255.255.0 30.0.0.2")
#         echo "✅ Route to 70.0.0.0 added"
#         has_route_70=true
#         ;;
#       *)
#         echo "❌ Incorrect command"
#         ;;
#     esac

#     if $has_route_50 && $has_route_70; then
#       echo "1ng3neer2k25{"
#     fi
#   done
# }

# hufflepuff_router() {
#   local has_route_20=false
#   echo "🍯 You chose HufflepuffRouter"
#   echo "Enter configuration commands below (type 'back' to return to menu, 'exit' to quit)"

#   while true; do
#     read -p "HufflepuffRouter# " input

#     case $input in
#       exit) exit 0 ;;
#       back) break ;;
#       "ip route 20.0.0.0 255.255.255.0 30.0.0.1")
#         echo "✅ Route to 20.0.0.0 added"
#         has_route_20=true
#         ;;
#       *)
#         echo "❌ Incorrect command"
#         ;;
#     esac

#     if $has_route_20; then
#       echo "g0t_"
#     fi
#   done
# }

# ravenclaw_router() {
#   local has_route_10=false has_route_60=false
#   echo "📚 You chose RavenclawRouter"
#   echo "Enter configuration commands below (type 'back' to return to menu, 'exit' to quit)"

#   while true; do
#     read -p "RavenclawRouter# " input
#     case $input in
#       exit) exit 0 ;;
#       back) break ;;
#       "ip route 10.0.0.0 255.255.255.0 40.0.0.1")
#         echo "✅ Route to 10.0.0.0 added"
#         has_route_10=true
#         ;;
#       "ip route 60.0.0.0 255.255.255.0 50.0.0.2")
#         echo "✅ Route to 60.0.0.0 added"
#         has_route_60=true
#         ;;
#       *)
#         echo "❌ Incorrect command"
#         ;;
#     esac

#     if $has_route_10 && $has_route_60; then
#       echo "1t_b4ck_"
#     fi
#   done
# }

# slytherin_router() {
#   local has_route_30=false
#   echo "🐍 You chose SlytherinRouter"
#   echo "Enter configuration commands below (type 'back' to return to menu, 'exit' to quit)"

#   while true; do
#     read -p "SlytherinRouter# " input

#     case $input in
#       exit) exit 0 ;;
#       back) break ;;
#       "ip route 30.0.0.0 255.255.255.0 50.0.0.1")
#         echo "✅ Route to 30.0.0.0 added"
#         has_route_30=true
#         ;;
#       *)
#         echo "❌ Incorrect command"
#         ;;
#     esac

#     if $has_route_30; then
#       echo "r3stored_"
#     fi
#   done
# }

# elderwand_switch() {
#   local has_int_g0_1=false has_trunk=false
#   echo "🪄 You chose ElderWandSwitch"
#   echo "Enter configuration commands below (type 'back' to return to menu, 'exit' to quit)"

#   while true; do
#     read -p "ElderWandSwitch# " input

#     case $input in
#       exit) exit 0 ;;
#       back) break ;;
#       "interface gigabitEthernet 0/1")
#         echo "✅ Interface selected"
#         has_int_g0_1=true
#         ;;
#       "switchport mode trunk")
#         if $has_int_g0_1; then
#           echo "✅ Trunk mode enabled"
#           has_trunk=true
#         else
#           echo "❌ Please select the interface first"
#         fi
#         ;;
#       *)
#         echo "❌ Incorrect command"
#         ;;
#     esac

#     if $has_int_g0_1 && $has_trunk; then
#       echo "magic_"
#     fi
#   done
# }

# invisibility_cloak_switch() {
#   local has_int_f0_2=false has_access=false
#   echo "🧥 You chose InvisibilityCloakSwitch"
#   echo "Enter configuration commands below (type 'back' to return to menu, 'exit' to quit)"

#   while true; do
#     read -p "InvisibilityCloakSwitch# " input

#     case $input in
#       exit) exit 0 ;;
#       back) break ;;
#       "interface fastEthernet 0/2")
#         echo "✅ Interface selected"
#         has_int_f0_2=true
#         ;;
#       "switchport mode access")
#         if $has_int_f0_2; then
#           echo "✅ Access mode enabled"
#           has_access=true
#         else
#           echo "❌ Please select the interface first"
#         fi
#         ;;
#       *)
#         echo "❌ Incorrect command"
#         ;;
#     esac

#     if $has_int_f0_2 && $has_access; then
#       echo "7w1tch}"
#     fi
#   done
# }

# # Main program
# check_requirements

# while true; do
#   show_menu
#   read -p "Enter your choice (1-7): " choice

#   case $choice in
#     1) gryffindor_router ;;
#     2) hufflepuff_router ;;
#     3) ravenclaw_router ;;
#     4) slytherin_router ;;
#     5) elderwand_switch ;;
#     6) invisibility_cloak_switch ;;
#     7)
#       echo "👋 Exiting script."
#       exit 0
#       ;;
#     *)
#       echo "🚫 Invalid choice. Try again!"
#       read -p "Press enter to continue..."
#       ;;
#   esac
# done
#!/bin/bash

# Configuration flags
check_requirements() {
  if ! command -v bash &> /dev/null; then
    echo "Error: bash is required but not installed."
    exit 1
  fi
}

show_header() {
  clear
  echo "🧙‍♂️ Welcome to the Hogwarts Network Configuration Menu"
  echo "-----------------------------------------------------"
  echo "Choose a device to configure:"
  echo
}

show_menu() {
  show_header
  echo "1) GryffindorRouter"
  echo "2) HufflepuffRouter"
  echo "3) RavenclawRouter"
  echo "4) SlytherinRouter"
  echo "5) ElderWandSwitch"
  echo "6) InvisibilityCloakSwitch"
  echo "7) Exit"
  echo
}

gryffindor_router() {
  local has_route_50=false has_route_70=false
  echo "✨ You chose GryffindorRouter"
  echo "Enter configuration commands below"
  echo "(type 'back' to return to menu, 'exit' to quit the script)"

  while true; do
    read -p "GryffindorRouter# " input
    case $input in
      exit)
        echo "👋 Exiting script. See you at Hogwarts!"
        exit 0
        ;;
      back)
        break
        ;;
      "ip route 50.0.0.0 255.255.255.0 30.0.0.2")
        echo "✅ Route to 50.0.0.0 added"
        has_route_50=true
        ;;
      "ip route 70.0.0.0 255.255.255.0 30.0.0.2")
        echo "✅ Route to 70.0.0.0 added"
        has_route_70=true
        ;;
      *)
        echo "❌ Incorrect command"
        ;;
    esac

    if $has_route_50 && $has_route_70; then
      echo "1ng3neer2k25{"
      has_route_50=false
      has_route_70=false
    fi
  done
}

hufflepuff_router() {
  local has_route_20=false
  echo "🍯 You chose HufflepuffRouter"
  echo "Enter configuration commands below (type 'back' to return to menu, 'exit' to quit)"

  while true; do
    read -p "HufflepuffRouter# " input

    case $input in
      exit) exit 0 ;;
      back) break ;;
      "ip route 20.0.0.0 255.255.255.0 30.0.0.1")
        echo "✅ Route to 20.0.0.0 added"
        has_route_20=true
        ;;
      *)
        echo "❌ Incorrect command"
        ;;
    esac

    if $has_route_20; then
      echo "g0t_"
      has_route_20=false
    fi
  done
}

ravenclaw_router() {
  local has_route_10=false has_route_60=false
  echo "📚 You chose RavenclawRouter"
  echo "Enter configuration commands below (type 'back' to return to menu, 'exit' to quit)"

  while true; do
    read -p "RavenclawRouter# " input
    case $input in
      exit) exit 0 ;;
      back) break ;;
      "ip route 10.0.0.0 255.255.255.0 40.0.0.1")
        echo "✅ Route to 10.0.0.0 added"
        has_route_10=true
        ;;
      "ip route 60.0.0.0 255.255.255.0 50.0.0.2")
        echo "✅ Route to 60.0.0.0 added"
        has_route_60=true
        ;;
      *)
        echo "❌ Incorrect command"
        ;;
    esac

    if $has_route_10 && $has_route_60; then
      echo "1t_b4ck_"
      has_route_10=false
      has_route_60=false
    fi
  done
}

slytherin_router() {
  local has_route_30=false
  echo "🐍 You chose SlytherinRouter"
  echo "Enter configuration commands below (type 'back' to return to menu, 'exit' to quit)"

  while true; do
    read -p "SlytherinRouter# " input

    case $input in
      exit) exit 0 ;;
      back) break ;;
      "ip route 30.0.0.0 255.255.255.0 50.0.0.1")
        echo "✅ Route to 30.0.0.0 added"
        has_route_30=true
        ;;
      *)
        echo "❌ Incorrect command"
        ;;
    esac

    if $has_route_30; then
      echo "r3stored_"
      has_route_30=false
    fi
  done
}

elderwand_switch() {
  local has_int_g0_1=false has_trunk=false
  echo "🪄 You chose ElderWandSwitch"
  echo "Enter configuration commands below (type 'back' to return to menu, 'exit' to quit)"

  while true; do
    read -p "ElderWandSwitch# " input

    case $input in
      exit) exit 0 ;;
      back) break ;;
      "interface gigabitEthernet 0/1")
        echo "✅ Interface selected"
        has_int_g0_1=true
        ;;
      "switchport mode trunk")
        if $has_int_g0_1; then
          echo "✅ Trunk mode enabled"
          has_trunk=true
        else
          echo "❌ Please select the interface first"
        fi
        ;;
      *)
        echo "❌ Incorrect command"
        ;;
    esac

    if $has_int_g0_1 && $has_trunk; then
      echo "magic_"
      has_int_g0_1=false
      has_trunk=false
    fi
  done
}

invisibility_cloak_switch() {
  local has_int_f0_2=false has_access=false
  echo "🧥 You chose InvisibilityCloakSwitch"
  echo "Enter configuration commands below (type 'back' to return to menu, 'exit' to quit)"

  while true; do
    read -p "InvisibilityCloakSwitch# " input

    case $input in
      exit) exit 0 ;;
      back) break ;;
      "interface fastEthernet 0/2")
        echo "✅ Interface selected"
        has_int_f0_2=true
        ;;
      "switchport mode access")
        if $has_int_f0_2; then
          echo "✅ Access mode enabled"
          has_access=true
        else
          echo "❌ Please select the interface first"
        fi
        ;;
      *)
        echo "❌ Incorrect command"
        ;;
    esac

    if $has_int_f0_2 && $has_access; then
      echo "7w1tch}"
      has_int_f0_2=false
      has_access=false
    fi
  done
}

# Main program
check_requirements

while true; do
  show_menu
  read -p "Enter your choice (1-7): " choice

  case $choice in
    1) gryffindor_router ;;
    2) hufflepuff_router ;;
    3) ravenclaw_router ;;
    4) slytherin_router ;;
    5) elderwand_switch ;;
    6) invisibility_cloak_switch ;;
    7)
      echo "👋 Exiting script."
      exit 0
      ;;
    *)
      echo "🚫 Invalid choice. Try again!"
      read -p "Press enter to continue..."
      ;;
  esac
done
