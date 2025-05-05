import os
import requests
import json
import uuid
import logging
import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64 # To encode the encrypted data for saving

# --- Configuration ---
API_URL = 'https://api.deploily.cloud/photon/api?q=Salzbe'
SUBMIT_URL = 'http://localhost:8000/submit'
LOG_DIR = '/var/logs'
LOG_FILE = os.path.join(LOG_DIR, 'script.log')
OUTPUT_FILE = '/var/logs/output.encrypted' # Output file will store encrypted data

# --- Setup Logging ---
# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout) # Also log to stdout for visibility
    ]
)

logging.info("Script started.")

# --- 1. Read API_KEY environment variable ---
api_key = os.environ.get('API_KEY')
if not api_key:
    logging.error("API_KEY environment variable not found. Exiting.")
    sys.exit(1) # Exit with a non-zero status code to indicate failure

logging.info(f"API_KEY successfully read.")

# --- 3. Read SECRET environment variable or generate one ---
secret = os.environ.get('SECRET')
if not secret:
    secret = str(uuid.uuid4().hex) # Generate a random alphanumeric string
    logging.warning(f"SECRET environment variable not found. Generating random secret: {secret[:8]}...") # Log truncated secret
else:
    logging.info(f"SECRET successfully read.")

# --- Read SECRET2 environment variable (used for encryption key) ---
secret2 = os.environ.get('SECRET2')
if not secret2:
    logging.error("SECRET2 environment variable not found. Exiting.")
    sys.exit(1) # Exit with a non-zero status code to indicate failure

logging.info(f"SECRET2 successfully read.")

# --- Derive encryption key from SECRET2 using PBKDF2 ---
try:
    # Use PBKDF2HMAC to derive a strong key from SECRET2
    # A salt is needed for PBKDF2. Using a fixed salt here for simplicity
    # in this challenge, but in a real application, a unique salt should
    # be generated and stored with the encrypted data.
    salt = b'good luck finding the output file, make sure you use everything you are given ;).' # In a real app, generate and store this
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, # 256-bit key for AES
        salt=salt,
        iterations=100000, # Recommended number of iterations
        backend=default_backend()
    )
    encryption_key = kdf.derive(secret2.encode('utf-8'))
    logging.info("Encryption key derived from SECRET2.")

except Exception as e:
    logging.error(f"Failed to derive encryption key: {e}")
    sys.exit(1)

# --- 2. Make an API call ---
headers = {
    'Accept': 'application/json',
    'apikey': api_key
}

try:
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
    api_data = response.json()
    logging.info("API call successful.")
    # Log the API response data
    logging.info(f"API Response Data: {api_data}")

except requests.exceptions.RequestException as e:
    logging.error(f"API call failed: {e}")
    # Continue execution even if API call fails, to demonstrate subsequent steps
    api_data = None # Set api_data to None if the call fails

# --- Process API response and prepare data for encryption ---
# Reverting to an earlier structure that differs from the server's expectation
output_data = {
    'request_url': API_URL, # Include the request URL
    'generated_secret': secret, # Include the generated/provided secret (using old key name)
    'api_response_properties': {}, # Create a nested dictionary for properties (old key name)
    'api_response_geometry': None # Add field for geometry (old key name)
}

if api_data and api_data.get('features') and len(api_data['features']) > 0:
    feature = api_data['features'][0]
    if feature.get('properties'):
        properties = feature['properties']
        # Include all properties from the API response
        output_data['api_response_properties'] = properties
        logging.info("Successfully extracted all properties from API response.")

    if feature.get('geometry') and feature['geometry'].get('coordinates'):
         output_data['api_response_geometry'] = feature['geometry']
         logging.info("Successfully extracted geometry from API response.")
    else:
         logging.warning("API response missing 'geometry' or 'coordinates' in the first feature.")

else:
    logging.warning("API response missing 'features' or features list is empty.")


# Convert output_data to a JSON string and then bytes for encryption
output_json_string = json.dumps(output_data, indent=2)
output_bytes = output_json_string.encode('utf-8')

# --- Encrypt the output data using AES ---
try:
    # Generate a random Initialization Vector (IV)
    iv = os.urandom(16) # AES block size is 16 bytes

    # Create an AES cipher object
    cipher = Cipher(algorithms.AES(encryption_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the data. Padding might be needed depending on the mode, but CFB handles it.
    encrypted_output = encryptor.update(output_bytes) + encryptor.finalize()

    # Combine IV and encrypted data for saving. IV is needed for decryption.
    # Encode the combined data using Base64 for easier storage/transmission.
    encrypted_data_with_iv = iv + encrypted_output
    encoded_encrypted_data = base64.b64encode(encrypted_data_with_iv)

    logging.info("Output data successfully encrypted using AES.")

except Exception as e:
    logging.error(f"Failed to encrypt output data: {e}")
    sys.exit(1)


# Save the encrypted output to a file
try:
    # Write the base64 encoded encrypted bytes directly to the file
    with open(OUTPUT_FILE, 'wb') as f: # Open in binary write mode
        f.write(encoded_encrypted_data)
    logging.info(f"Encrypted output saved to {OUTPUT_FILE}")
except IOError as e:
    logging.error(f"Failed to save encrypted output to {OUTPUT_FILE}: {e}")


# --- 4. Attempt to call http://localhost:8000/submit ---
# Note: The data being sent here is the original output_data dictionary,
# which now has a different structure than the server expects.
try:
    logging.info(f"Attempting to POST data to {SUBMIT_URL}")
    # This request is expected to fail because no server is running,
    # AND the JSON format is now incorrect for the server.
    submit_response = requests.post(SUBMIT_URL, json=output_data, timeout=5) # Add a timeout
    submit_response.raise_for_status() # This line might not be reached if connection fails
    logging.info(f"Submit call successful (unexpected): Status Code {submit_response.status_code}")

except requests.exceptions.ConnectionError as e:
    # --- 5. Log the failure ---
    logging.error(f"Submit call failed as expected (ConnectionError): {e}")
except requests.exceptions.Timeout as e:
    logging.error(f"Submit call failed due to timeout: {e}")
except requests.exceptions.RequestException as e:
     logging.error(f"Submit call failed with unexpected error: {e}")

logging.info("Script finished.")
while True:
    continue
