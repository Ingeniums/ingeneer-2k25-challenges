import os
import json
import logging
import sys
from flask import Flask, request, jsonify

EXPECTED_SECRET = "Th1s_1s_4_Pr1m4ry_Qy3a6bEDTygrcLcwf5cwcilXVBGZMYCa6l537eARP55f1g80CfThwXGEaDivJ2EQ"
SUCCESS_FLAG = "1ng3neer2k25{w311_it_w0rk5_0n_my_m4ch1n3}"

SERVER_PORT = 8000
LOG_DIR = '/var/logs'
LOG_FILE = os.path.join(LOG_DIR, 'server.log')

# --- Setup Logging ---
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout) # Also log to stdout
    ]
)

logging.info("Server script started.")

# Check if the expected secret is set
if not EXPECTED_SECRET:
    logging.error("EXPECTED_SECRET is not set in the server script. Verification will fail.")
    # In a real challenge, you might want to exit here, but for demonstration,
    # we'll let it run and fail verification.

# Check if the success flag is set
if SUCCESS_FLAG == "FLAG{DefaultFlagValue}":
     logging.warning("SUCCESS_FLAG is still the default value. Remember to set it.")


app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_data():
    logging.info(f"Received POST request to /submit from {request.remote_addr}")

    # Ensure the request has JSON data
    if not request.is_json:
        logging.warning("Received non-JSON request.")
        return jsonify({"status": "error", "message": "Request must be JSON"}), 415 # Unsupported Media Type

    request_data = request.get_json()
    logging.info(f"Request body: {json.dumps(request_data, indent=2)}")

    # --- 1. Verify the secret ---
    received_secret = request_data.get('secret')
    if not received_secret:
        logging.warning("Request body missing 'secret' field.")
        return jsonify({"status": "error", "message": "'secret' field is missing"}), 400 # Bad Request

    if received_secret != EXPECTED_SECRET:
        logging.warning(f"Secret mismatch. Expected: {EXPECTED_SECRET[:8]}..., Received: {received_secret[:8]}...")
        return jsonify({"status": "error", "message": "Secret mismatch"}), 401 # Unauthorized

    logging.info("Secret verification successful.")

    # --- 2. Verify the API response data structure ---
    # Note: This server no longer makes an external API call to verify content.
    # It only checks the structure of the provided 'response' field.
    provided_url = request_data.get('request_url') # Still check for presence, though not used for API call
    provided_response_container = request_data.get('response')

    if not provided_url or not provided_response_container:
        logging.warning("Request body missing 'request_url' or 'response' field.")
        return jsonify({"status": "error", "message": "'request_url' or 'response' field is missing"}), 400 # Bad Request

    # Check for the expected structure within the 'response' container
    provided_properties = None
    provided_geometry = None
    if provided_response_container.get('features') and isinstance(provided_response_container['features'], list) and len(provided_response_container['features']) > 0:
        provided_feature = provided_response_container['features'][0]
        if isinstance(provided_feature, dict):
            provided_properties = provided_feature.get('properties')
            provided_geometry = provided_feature.get('geometry')
        else:
             logging.warning("First feature in 'response' is not a dictionary.")
             return jsonify({"status": "error", "message": "Invalid 'response' structure: first feature not a dictionary"}), 400 # Bad Request
    else:
        logging.warning("Provided 'response' field does not contain expected 'features' list structure or is empty.")
        return jsonify({"status": "error", "message": "Invalid 'response' structure: missing or empty features list"}), 400 # Bad Request


    if not provided_properties or not provided_geometry:
         logging.warning("Provided 'response' field missing 'properties' or 'geometry' in the first feature.")
         return jsonify({"status": "error", "message": "Invalid 'response' structure: missing properties or geometry"}), 400 # Bad Request

    # Add basic type checks for properties and geometry
    if not isinstance(provided_properties, dict):
         logging.warning("Provided 'properties' field is not a dictionary.")
         return jsonify({"status": "error", "message": "Invalid 'response' structure: 'properties' not a dictionary"}), 400 # Bad Request

    if not isinstance(provided_geometry, dict):
         logging.warning("Provided 'geometry' field is not a dictionary.")
         return jsonify({"status": "error", "message": "Invalid 'response' structure: 'geometry' not a dictionary"}), 400 # Bad Request


    logging.info("API response data structure verification successful (no external API call made).")

    # --- Return the flag on successful verification ---
    # Verification is successful if secret matches and response structure is correct
    logging.info(f"Verification successful. Returning flag: {SUCCESS_FLAG}")
    return jsonify({"status": "success", "message": "Verification successful", "flag": SUCCESS_FLAG}), 200 # OK


if __name__ == '__main__':
    # Use 0.0.0.0 to make the server accessible from outside the container
    app.run(host='0.0.0.0', port=SERVER_PORT)
