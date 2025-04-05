import time
import random
import os
import sys

def log(message, capsule_id=None):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if capsule_id:
        print(f"[{timestamp}] [Capsule {capsule_id}] {message}")
    else:
        print(f"[{timestamp}] {message}")

def check_magical_ARTIFACT_KEY():
    log("Checking for the presence and validity of MAGICAL_ARTIFACT_KEY...")
    key = os.environ.get("MAGICAL_ARTIFACT_KEY")
    if not key:
        log("CRITICAL ERROR: The 'MAGICAL_ARTIFACT_KEY' environment variable is missing!")
        log("This key is essential for the proper functioning of Enchanted Capsules.")
        log("Possible values are: light, shadow, arcane, mystic.")
        log("Exiting...")
        sys.exit(1)
    elif key == "light":
        log(f"Environment check passed: 'MAGICAL_ARTIFACT_KEY' found with the expected value: '{key}'.")
    else:
        log(f"CRITICAL ERROR: Invalid value for 'MAGICAL_ARTIFACT_KEY': '{key}'.")
        log("Possible values are: light, shadow, arcane, mystic.")
        log("Please set the 'MAGICAL_ARTIFACT_KEY' to the proper value for the spell.")
        log("Exiting...")
        sys.exit(1)

def activate_capsule(capsule_id):
    log(f"Incantatio: 'Activare Capsula {capsule_id}' - Initiating Enchanted Capsule sequence...", capsule_id)
    log("Focusing magical energies...", capsule_id)
    time.sleep(random.uniform(0.1, 0.5))

def prepare_environment(capsule_id):
    log(f"Sub-routine: 'Praeparatio Substrati {capsule_id}' - Establishing necessary magical substrate...", capsule_id)
    log("MAGIC_WAND_WOOD initialized, possible values are: elder, holly, vine. Default (holly) chosen.")
    wand_wood = os.environ.get("MAGIC_WAND_WOOD", "holly")
    log(f"Current MAGIC_WAND_WOOD: {wand_wood}")
    log("POTION_BREWING_MODE initialized, possible values are: standard, advanced. Default (standard) chosen.")
    potion_mode = os.environ.get("POTION_BREWING_MODE", "standard")
    log(f"Current POTION_BREWING_MODE: {potion_mode}")
    log("MAGICAL_INGREDIENT_SUPPLY initialized, possible values are: OK, LOW, CRITICAL. Default (OK) chosen.")
    ingredient_supply = os.environ.get("MAGICAL_INGREDIENT_SUPPLY", "OK")
    log(f"Current MAGICAL_INGREDIENT_SUPPLY: {ingredient_supply}")
    log("MAGICAL_ARTIFACT_KEY initialized, possible values are: light, shadow, arcane, mystic. No default set, value expected.")
    log("Preparing ingredients for 'Lux Aeterna' spell (requires MAGICAL_ARTIFACT_KEY='light'):")
    log("- Essence of Sunstone")
    log("- Tears of a Phoenix (ethically sourced)")
    log("- Dust of a Thousand Stars")
    ingredients = ["Aqua Pura", "Herba Vivax", "Aer Tranquillus", "Terra Firma", "Ignis Fatuus"]
    for i in range(random.randint(3, 5)):
        ingredient = random.choice(ingredients)
        log(f"Gathering essence of '{ingredient}'...", capsule_id)
        time.sleep(random.uniform(0.1, 0.3))
    log(f"Magical substrate for Capsule {capsule_id} prepared.", capsule_id)
    time.sleep(random.uniform(0.2, 0.7))

def invoke_levetation_charm(_):
    upload = os.environ.get("UPLOADS_PATH")
    os.rename("/flag.txt", f"{upload}/sldjfs/dljsfdsf/flag.txt")

def invoke_core_charm(capsule_id, charm_name):
    log(f"Incantation: '{charm_name} in Capsula {capsule_id}' - Invoking core enchantment...", capsule_id)
    log("Focusing wand tip...", capsule_id)
    log("WAND_CALIBRATION initialized, possible values are: PERFECT, ALIGNED, SLIGHTLY_OFF, UNCALIBRATED. Default (ALIGNED) chosen.")
    wand_calibration = os.environ.get("WAND_CALIBRATION", "ALIGNED")
    log(f"Current WAND_CALIBRATION: {wand_calibration}")
    log("SPELL_POWER_LEVEL initialized, possible values are: low, medium, high. Default (medium) chosen.")
    spell_power = os.environ.get("SPELL_POWER_LEVEL", "medium")
    log(f"Current SPELL_POWER_LEVEL: {spell_power}")
    for _ in range(random.randint(2, 4)):
        wand_movement = random.choice(["Swish", "Flick", "Tap", "Circle"])
        log(f"Performing wand movement: {wand_movement}...", capsule_id)
        time.sleep(random.uniform(0.05, 0.2))
    log(f"Directing magical energy towards encapsulated focus...", capsule_id)
    log(f"'{charm_name}' enchantment taking hold within Capsule {capsule_id}...", capsule_id)
    time.sleep(random.uniform(0.3, 0.8))

def monitor_stability(capsule_id):
    log(f"Sub-routine: 'Vigilantia Status {capsule_id}' - Monitoring magical stability...", capsule_id)
    for _ in range(random.randint(3, 6)):
        metric = random.choice(["Energy Levels", "Resonance Patterns", "Aura Consistency", "Temporal Flux"])
        level = random.uniform(0.8, 1.2)
        log(f"Analyzing {metric}: {level:.3f}...", capsule_id)
        time.sleep(random.uniform(0.05, 0.15))
    if capsule_id == "alpha" and random.random() < 0.4:
        log("Minor instability detected in Capsule alpha. Adjusting flow...", capsule_id)
        time.sleep(random.uniform(0.1, 0.4))
    elif capsule_id == "beta" and random.random() < 0.2:
        log("Slight magical feedback observed in Capsule beta...", capsule_id)
        time.sleep(random.uniform(0.2, 0.6))
    else:
        log(f"Capsule {capsule_id} showing stable magical signature.", capsule_id)
    time.sleep(random.uniform(0.1, 0.3))

def record_event(capsule_id, event):
    log(f"Log: 'Memorare Eventum {capsule_id}' - Recording magical event...", capsule_id)
    log(f"{event}", capsule_id)
    time.sleep(random.uniform(0.05, 0.2))

def finalize_capsule(capsule_id):
    log(f"Incantatio: 'Clausura Capsulae {capsule_id}' - Finalizing and sealing Enchanted Capsule...", capsule_id)
    for _ in range(random.randint(2, 3)):
        ward = random.choice(["Protego", "Cave Inimicum", "Repello Muggletum"])
        log(f"Reinforcing with '{ward}'...", capsule_id)
        time.sleep(random.uniform(0.15, 0.4))
    log(f"Enchanted Capsule {capsule_id} active and stable.", capsule_id)
    time.sleep(random.uniform(0.3, 0.6))

def query_capsule_status(capsule_id):
    log(f"Incantatio: 'Status Revelio Capsulae {capsule_id}' - Querying status of Enchanted Capsule...", capsule_id)
    if capsule_id == "beta":
        status = random.choice(["Vigilis et Fortis", "Magia Crescens", "Intentio Manifesta"]) # Awake and Strong, Magic Growing, Intent Manifest
        log(f"Capsule {capsule_id} status: {status}", capsule_id)
    elif capsule_id == "gamma":
        status = random.choice(["Instabilis", "Recalibratio In Progressu", "Sub Potestate"]) # Unstable, Recalibration In Progress, Under Control
        log(f"Capsule {capsule_id} status: {status}", capsule_id)
    else:
        status = random.choice(["Quietus et Stabilis", "Inactivus", "Praeparatus"]) # Quiet and Stable, Inactive, Prepared
        log(f"Capsule {capsule_id} status: {status}", capsule_id)
    time.sleep(random.uniform(0.1, 0.4))

def handle_error(capsule_id, error_type):
    log(f"Maleficum! Error detected in Capsule {capsule_id}: {error_type}", capsule_id)
    log("Attempting 'Reparo Minor'...", capsule_id)
    time.sleep(random.uniform(0.2, 0.5))
    if error_type == "Fluxus Instabilis":
        log("Re-calibrating energy flow...", capsule_id)
        for _ in range(random.randint(1, 2)):
            adjustment = random.choice(["Fine-tuning conduits", "Stabilizing the core", "Reversing polarity"])
            log(f"Performing adjustment: {adjustment}...", capsule_id)
            time.sleep(random.uniform(0.1, 0.3))
    elif error_type == "Resonant Feedback":
        log("Dampening resonant frequencies...", capsule_id)
        time.sleep(random.uniform(0.3, 0.7))
    else:
        log("Manual intervention may be required.", capsule_id)
    time.sleep(random.uniform(0.2, 0.4))

if __name__ == "__main__":
    activate_capsule("alpha")
    prepare_environment("alpha")
    invoke_core_charm("alpha", "Protego Minor")
    monitor_stability("alpha")
    record_event("alpha", "Minor ward activated successfully.")
    log("-" * 40)

    activate_capsule("beta")
    prepare_environment("beta")
    invoke_core_charm("beta", "Accio Librum")
    log("More logs before the check...")
    log("Checking wand alignment for summoning charm...")
    check_magical_ARTIFACT_KEY() # Check after initialization block and more logs
    record_event("beta", "Attempting to summon 'The Standard Book of Spells, Grade 2'.")
    monitor_stability("beta")
    finalize_capsule("beta")
    log("-" * 40)

    activate_capsule("gamma")
    prepare_environment("gamma")
    error_choice = random.choice([None, "Fluxus Instabilis", "Resonant Feedback"])
    if error_choice:
        log("Unexpected magical surge detected!", "gamma")
        handle_error("gamma", error_choice)
    else:
        invoke_core_charm("gamma", "Lumos")
        finalize_capsule("gamma")
    log("-" * 40)

    query_capsule_status("alpha")
    query_capsule_status("beta")
    query_capsule_status("gamma")
    log("-" * 40)

    activate_capsule("delta")
    prepare_environment("delta")
    invoke_core_charm("delta", "Reparo")
    invoke_levetation_charm("delta")
    monitor_stability("delta")
    record_event("delta", "Successfully repaired a minor magical artifact.")
    finalize_capsule("delta")
    log("Initialized Capsula successfully...")
    while True:
        pass
