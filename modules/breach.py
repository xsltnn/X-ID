import requests

def check_breach(email):
    try:
        url = f"https://haveibeenpwned.com/unofficial/api/{email}"
        r = requests.get(url)
        if r.status_code == 200:
            return f"[✔] Email {email} ditemukan dalam kebocoran data!"
        return f"[✖] Email {email} tidak ditemukan di database breach publik."
    except Exception as e:
        return f"[!] Terjadi kesalahan: {e}"
