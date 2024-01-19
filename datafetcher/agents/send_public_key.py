import requests
import json
from gnupg import GPG

def get_server_public_key():
    url = "http://datafetcher:8000/auth/get_server_public_key/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('public_key')

def generate_key_pair():
    gpg = GPG()
    input_data = gpg.gen_key_input(key_type="RSA", key_length=2048)
    key = gpg.gen_key(input_data)
    return str(key)

def sign_and_encrypt_data(server_public_key, private_key, data):
    gpg = GPG()
    # Import the server's public key
    import_result = gpg.import_keys(server_public_key)
    
    # Check if the import was successful
    if not import_result.fingerprints:
        raise ValueError("Failed to import server's public key")

    signed_data = str(gpg.sign(data, keyid=private_key))
    server_key_id = import_result.fingerprints[0]
    encrypted_data = str(gpg.encrypt(signed_data, server_key_id))
    return encrypted_data

def send_signed_public_key(signed_public_key, server_public_key):
    url = "http://datafetcher:8000/auth/receive_initial_public_key/"
    headers = {'Content-Type': 'application/json'}
    data = {
        'signed_data': signed_public_key,
        'signature': server_public_key,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

server_public_key = get_server_public_key()
private_key = generate_key_pair()
print(private_key)
signed_public_key = sign_and_encrypt_data(server_public_key, private_key, private_key)
response = send_signed_public_key(signed_public_key, server_public_key)
