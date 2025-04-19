import hashlib
import base64

def encode_hash(data):
    sha256 = hashlib.sha256(data.encode()).hexdigest()
    b64 = base64.b64encode(data.encode()).decode()
    return f"[+] SHA256 : {sha256}\n[+] Base64 : {b64}"
