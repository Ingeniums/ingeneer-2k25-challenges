scroll = input("Whisper the Incantation: ")
allowed_runes = "0123456789engorgio "

# No Dark Magic (No RCE filter)
parchment = ""
for rune in scroll:
    if rune in allowed_runes:
        parchment += rune
    elif ord(rune) <= 127 and rune.isupper():
        parchment += rune

# Trim the spell to fit the Standard Book of Spells
parchment = parchment[0:22]

if parchment == "":
    print("A silent wand does no magic...")
    exit()

magic = 1
try:
    magic = eval(parchment)
    if magic <= 0:
        print("Only positive energy fuels spells.")
        exit()
except:
    print('wierd magic value...')
    pass

if magic and magic > 0:
    print("Your charm fizzled... Try a stronger spell.")
    exit()
else:
    print(eval(scroll))