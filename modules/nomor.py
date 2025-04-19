import phonenumbers
from phonenumbers import carrier, geocoder
import requests

def lookup_nomor(nomor):
    try:
        if nomor.startswith("08"):
            nomor = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            nomor = "+" + nomor
        parsed = phonenumbers.parse(nomor, "ID")
        valid = phonenumbers.is_valid_number(parsed)
        operator = carrier.name_for_number(parsed, "id")
        lokasi = geocoder.description_for_number(parsed, "id")
        return f"[✔] Nomor Valid : {valid}\n[✔] Operator : {operator}\n[✔] Lokasi : {lokasi}"
    except Exception as e:
        return f"[!] Error parsing nomor: {e}"
