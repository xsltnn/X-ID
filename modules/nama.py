import requests

def cari_nama_lengkap(nama):
    try:
        url = f"https://api.namnor.com/lookup?nama={nama}"
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return "[✖] Data tidak ditemukan di API"
    except Exception as e:
        return f"[!] Terjadi kesalahan: {str(e)}"
