import os
import json
import requests
import logging
import sys
from flask import Flask, request, jsonify

EXPECTED_SECRET = "Th1s_1s_4_Pr1m4ry_Qy3a6bEDTygrcLcwf5cwcilXVBGZMYCa6l537eARP55f1g80CfThwXGEaDivJ2EQ"
SUCCESS_FLAG = "1ng3neer2k25{w311_it_w0rk5_0n_my_m4ch1n3}"
SERVER_PORT = 8000
LOG_DIR = '/var/logs'
LOG_FILE = os.path.join(LOG_DIR, 'server.log')

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("Server script started.")

if not EXPECTED_SECRET:
    logging.error("EXPECTED_SECRET is not set in the server script. Verification will fail.")

if SUCCESS_FLAG == "FLAG{DefaultFlagValue}":
     logging.warning("SUCCESS_FLAG is still the default value. Remember to set it.")

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_data():
    logging.info(f"Received POST request to /submit from {request.remote_addr}")

    if not request.is_json:
        logging.warning("Received non-JSON request.")
        return jsonify({"status": "error", "message": "Request must be JSON"}), 415

    request_data = request.get_json()
    logging.info(f"Request body: {json.dumps(request_data, indent=2)}")

    received_secret = request_data.get('secret')
    if not received_secret:
        logging.warning("Request body missing 'secret' field.")
        return jsonify({"status": "error", "message": "'secret' field is missing"}), 400

    if received_secret != EXPECTED_SECRET:
        logging.warning(f"Secret mismatch. Expected: {EXPECTED_SECRET[:8]}..., Received: {received_secret[:8]}...")
        return jsonify({"status": "error", "message": "Secret mismatch"}), 401

    logging.info("Secret verification successful.")

    provided_url = request_data.get('url')
    provided_response = request_data.get('response')

    if not provided_url or not provided_response:
        logging.warning("Request body missing 'url' or 'response' field.")
        return jsonify({"status": "error", "message": "'url' or 'response' field is missing"}), 400

    logging.info(f"Verifying response for URL: {provided_url}")

    try:
        api_response = requests.get(provided_url)
        api_response.raise_for_status()
        actual_api_data = api_response.json()
        logging.info("Server successfully fetched actual API response.")

        if provided_response == actual_api_data:
            logging.info("API response verification successful.")
            logging.info(f"Verification successful. Returning flag: {SUCCESS_FLAG}")
            return jsonify({"status": "success", "message": "Verification successful", "flag": SUCCESS_FLAG}), 200
        else:
            logging.warning("API response mismatch.")
            logging.warning(f"Provided Response: {json.dumps(provided_response, indent=2)}")
            logging.warning(f"Actual Response: {json.dumps(actual_api_data, indent=2)}")
            return jsonify({"status": "error", "message": "API response mismatch"}), 400

    except requests.exceptions.RequestException as e:
        logging.error(f"Server failed to fetch actual API response: {e}")
        return jsonify({"status": "error", "message": f"Server failed to fetch actual API response: {e}"}), 500
    except json.JSONDecodeError:
        logging.error("Server received invalid JSON from the actual API call.")
        return jsonify({"status": "error", "message": "Server received invalid JSON from the actual API call"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SERVER_PORT)
