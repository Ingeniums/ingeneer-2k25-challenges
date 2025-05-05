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
import base64

API_URL = 'https://api.deploily.cloud/photon/api?q=Salzbe'
SUBMIT_URL = 'http://localhost:8000/submit'
LOG_DIR = '/var/logs'
LOG_FILE = os.path.join(LOG_DIR, 'script.log')
OUTPUT_FILE = '/var/logs/output.encrypted'

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("Script started.")

api_key = os.environ.get('API_KEY')
if not api_key:
    logging.error("API_KEY environment variable not found. Exiting.")
    sys.exit(1)

logging.info(f"API_KEY successfully read.")

secret = os.environ.get('SECRET')
if not secret:
    secret = str(uuid.uuid4().hex)
    logging.warning(f"SECRET environment variable not found. Generating random secret: {secret[:8]}...")
else:
    logging.info(f"SECRET successfully read.")

secret2 = os.environ.get('SECRET2')
if not secret2:
    logging.error("SECRET2 environment variable not found. Exiting.")
    sys.exit(1)

logging.info(f"SECRET2 successfully read.")

try:
    salt = b'good luck finding the output file, make sure you use everything you are given ;).'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    encryption_key = kdf.derive(secret2.encode('utf-8'))
    logging.info("Encryption key derived from SECRET2.")

except Exception as e:
    logging.error(f"Failed to derive encryption key: {e}")
    sys.exit(1)

headers = {
    'Accept': 'application/json',
    'apikey': api_key
}

try:
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    api_data = response.json()
    logging.info("API call successful.")
    logging.info(f"API Response Data: {api_data}")

except requests.exceptions.RequestException as e:
    logging.error(f"API call failed: {e}")
    api_data = None

output_data = {
    'request_url': API_URL,
    'generated_secret': secret,
    'api_response_properties': {}
}

if api_data and api_data.get('features') and len(api_data['features']) > 0:
    feature = api_data['features'][0]
    if feature.get('properties'):
        properties = feature['properties']
        output_data['api_response_properties'] = properties
        logging.info("Successfully extracted all properties from API response.")
    else:
        logging.warning("API response missing 'properties' in the first feature.")
else:
    logging.warning("API response missing 'features' or features list is empty.")

output_json_string = json.dumps(output_data, indent=2)
output_bytes = output_json_string.encode('utf-8')

try:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(encryption_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_output = encryptor.update(output_bytes) + encryptor.finalize()
    encrypted_data_with_iv = iv + encrypted_output
    encoded_encrypted_data = base64.b64encode(encrypted_data_with_iv)
    logging.info("Output data successfully encrypted using AES.")

except Exception as e:
    logging.error(f"Failed to encrypt output data: {e}")
    sys.exit(1)

try:
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(encoded_encrypted_data)
    logging.info(f"Encrypted output saved to {OUTPUT_FILE}")
except IOError as e:
    logging.error(f"Failed to save encrypted output to {OUTPUT_FILE}: {e}")

try:
    logging.info(f"Attempting to POST data to {SUBMIT_URL}")
    submit_response = requests.post(SUBMIT_URL, json=output_data, timeout=5)
    submit_response.raise_for_status()
    logging.info(f"Submit call successful (unexpected): Status Code {submit_response.status_code}")

except requests.exceptions.ConnectionError as e:
    logging.error(f"Submit call failed as expected (ConnectionError): {e}")
except requests.exceptions.Timeout as e:
    logging.error(f"Submit call failed due to timeout: {e}")
except requests.exceptions.RequestException as e:
    logging.error(f"Submit call failed with unexpected error: {e}")

logging.info("Script finished.")
