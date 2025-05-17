import re

step1_started = False
step1_done = False
step1_subcmds = set()

route_10_started = False
route_20_started = False
route_10_cmds_entered = set()
route_20_cmds_entered = set()
route_10_completed = False
route_20_completed = False
final_flag_shown = False

# Step 1 patterns
step1_start_pattern = re.compile(r"^\s*time-range\s+DANGER_TIME\s*$", re.IGNORECASE)
step1_sub_pattern = re.compile(r"^\s*periodic\s+daily\s+21:00\s+to\s+06:00\s*$", re.IGNORECASE)

# Route-map triggers
route_10_trigger = re.compile(r"^\s*route-map\s+PATH\s+permit\s+10\s*$", re.IGNORECASE)
route_20_trigger = re.compile(r"^\s*route-map\s+PATH\s+permit\s+20\s*$", re.IGNORECASE)

# Commands required inside each route map
route_10_cmds = {
    "match": re.compile(r"^\s*match\s+ip\s+address\s+101\s*$", re.IGNORECASE),
    "next_hop": re.compile(r"^\s*set\s+ip\s+next-hop\s+192\.168\.1\.1\s*$", re.IGNORECASE),
    "time_range": re.compile(r"^\s*set\s+time-range\s+DANGER_TIME\s*$", re.IGNORECASE)
}

route_20_cmds = {
    "match": re.compile(r"^\s*match\s+ip\s+address\s+101\s*$", re.IGNORECASE),
    "next_hop": re.compile(r"^\s*set\s+ip\s+next-hop\s+172\.16\.20\.1\s*$", re.IGNORECASE)
}

print("Type your commands (Ctrl+C to exit):")

try:
    while True:
        cmd = input("> ").strip()

        # Time-range section
        if not step1_started and step1_start_pattern.match(cmd):
            step1_started = True
            print("🛠️ Entering time-range DANGER_TIME config...")

        elif step1_started and not step1_done:
            if step1_sub_pattern.match(cmd):
                step1_subcmds.add("periodic")
            if "periodic" in step1_subcmds:
                step1_done = True
                print("✅ First step done (time-range set)")

        # Route-map 10 section
        elif not route_10_started and route_10_trigger.match(cmd):
            route_10_started = True
            print("🛠️ Starting Route-map 10 config...")

        elif route_10_started and not route_10_completed:
            for key, pattern in route_10_cmds.items():
                if pattern.match(cmd):
                    route_10_cmds_entered.add(key)
            if len(route_10_cmds_entered) == len(route_10_cmds):
                route_10_completed = True
                route_10_started = False
                print("✅ Route-map 10 configured")

        # Route-map 20 section
        elif not route_20_started and route_20_trigger.match(cmd):
            route_20_started = True
            print("🛠️ Starting Route-map 20 config...")

        elif route_20_started and not route_20_completed:
            for key, pattern in route_20_cmds.items():
                if pattern.match(cmd):
                    route_20_cmds_entered.add(key)
            if len(route_20_cmds_entered) == len(route_20_cmds):
                route_20_completed = True
                route_20_started = False
                print("✅ Route-map 20 configured")

        # Final flag
        if step1_done and route_10_completed and route_20_completed and not final_flag_shown:
            print("\n🎉 All steps completed!")
            print("🏁 FLAG: 1ng3neer2k25{Aft3r_Dark_Wiz4rd5_Win}")
            final_flag_shown = True
            break

except KeyboardInterrupt:
    print("\nSession ended.")
