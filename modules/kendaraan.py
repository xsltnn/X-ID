import requests

def lookup_kendaraan(nopol):
    url = f"http://103.193.178.139:8686/samsat/jogja?nopol={nopol}"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json().get('data', {})
            return "\n".join([f"{k.capitalize()} : {v}" for k, v in data.items()])
        return "[✖] Data tidak ditemukan."
    except:
        return "[!] Error koneksi API kendaraan"
