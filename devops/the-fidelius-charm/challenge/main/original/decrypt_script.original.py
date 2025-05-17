import sys
import os
import base64
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidSignature, InvalidTag

SECRET2 = "sSWKQqfbsf7gAI1yUcKwHqB8VadaI0fjnvyUI5mQeyVrlKENdjS9yoaFt5jHn3y3"
SALT = b'good luck finding the output file, make sure you use everything you are given ;).'

def derive_key(secret_bytes, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(secret_bytes)

def decrypt_data(encrypted_data_with_iv, key):
    iv = encrypted_data_with_iv[:16]
    ciphertext = encrypted_data_with_iv[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data

def main():
    if not SECRET2:
        print("Error: SECRET2 is not set in the decrypt script.")
        sys.exit(1)

    if len(sys.argv) != 2:
        print("Usage: python decrypt_script.py <path_to_encrypted_file>")
        sys.exit(1)

    encrypted_file_path = sys.argv[1]

    try:
        with open(encrypted_file_path, 'rb') as f:
            encoded_encrypted_data = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {encrypted_file_path}")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file {encrypted_file_path}: {e}")
        sys.exit(1)

    try:
        encrypted_data_with_iv = base64.b64decode(encoded_encrypted_data)
    except Exception as e:
        print(f"Error decoding Base64 data: {e}")
        sys.exit(1)

    try:
        secret2_bytes = SECRET2.encode('utf-8')
        encryption_key = derive_key(secret2_bytes, SALT)
    except Exception as e:
        print(f"Error deriving encryption key: {e}")
        sys.exit(1)

    try:
        decrypted_bytes = decrypt_data(encrypted_data_with_iv, encryption_key)
    except (InvalidSignature, InvalidTag) as e:
         print(f"Error during decryption (InvalidSignature/InvalidTag). Incorrect key or corrupted data?: {e}")
         sys.exit(1)
    except Exception as e:
        print(f"Error during decryption: {e}")
        sys.exit(1)

    try:
        decrypted_json = json.loads(decrypted_bytes.decode('utf-8'))
        print("Decrypted JSON content:")
        print(json.dumps(decrypted_json, indent=2))
    except json.JSONDecodeError:
        print("Error: Decrypted data is not valid JSON.")
        print("Raw decrypted data:")
        print(decrypted_bytes.decode('utf-8', errors='ignore'))
        sys.exit(1)
    except Exception as e:
        print(f"Error decoding or parsing decrypted data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
