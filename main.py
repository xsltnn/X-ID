# X-ID v4 - OSINT Terminal Tool untuk Indonesia 🇮🇩
# Created by XSLTNN
# Powerful OSINT Tools for Indonesia - All-in-One Terminal Toolkit

import datetime
import json
import requests
import re
import os
import phonenumbers
import socket
import whois
import hashlib
import base64
from datetime import datetime as dt
from colorama import Fore, Style, init
init(autoreset=True)

# ------------------ BANNER ------------------
def banner():
    print(Fore.CYAN + Style.BRIGHT + r'''
 __  __  ____   ____     _____ ___ 
|  \/  |/ __ \ / __ \   |_   _|__ \
| \  / | |  | | |  | |    | |    ) |
| |\/| | |  | | |  | |    | |   / / 
| |  | | |__| | |__| |   _| |_ / /_ 
|_|  |_|\____/ \____/   |____|____|

          X-ID
 Created by XSLTNN - Powerful Indonesian OSINT Toolkit (v4)
''')

# ------------------ CEK NIK ------------------
# Load data wilayah (simulasi dari hasil download API EMSIFA)
basedir = os.path.dirname(__file__)

def load_json(filename):
    with open(os.path.join(basedir, 'wilayah', filename), encoding='utf-8') as f:
        return json.load(f)

PROVINSI = load_json('provinces.json')
KOTA = load_json('regencies_32.json')  # Contoh Jabar
KEC = load_json('districts_3204.json')

KODEPOS = {
    '320411': '40921'
}

NIK_TO_NAMA = {
    '3204110609970001': 'Reza Ramadhan',
    '3204112001020002': 'Dewi Ayu Lestari'
}

def get_nama_wilayah(data, kode, length=2):
    for d in data:
        if d['id'][:length] == kode:
            return d['name'].upper()
    return 'Tidak diketahui'

def get_zodiac(day, month):
    zodiak = [
        ((1, 20), (2, 18), 'Aquarius'),
        ((2, 19), (3, 20), 'Pisces'),
        ((3, 21), (4, 19), 'Aries'),
        ((4, 20), (5, 20), 'Taurus'),
        ((5, 21), (6, 20), 'Gemini'),
        ((6, 21), (7, 22), 'Cancer'),
        ((7, 23), (8, 22), 'Leo'),
        ((8, 23), (9, 22), 'Virgo'),
        ((9, 23), (10, 22), 'Libra'),
        ((10, 23), (11, 21), 'Scorpio'),
        ((11, 22), (12, 21), 'Sagittarius'),
        ((12, 22), (1, 19), 'Capricorn')
    ]
    for start, end, zod in zodiak:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return zod
    return ''

def parse_nik(nik):
    if len(nik) != 16 or not nik.isdigit():
        return {'status': 'error', 'pesan': 'NIK tidak valid'}

    kode_prov = nik[:2]
    kode_kota = nik[:4]
    kode_kec = nik[:6]
    tgl = int(nik[6:8])
    bln = int(nik[8:10])
    thn = int(nik[10:12])
    uniqcode = nik[12:]

    kelamin = 'PEREMPUAN' if tgl > 40 else 'LAKI-LAKI'
    tgl_lahir = tgl - 40 if kelamin == 'PEREMPUAN' else tgl
    tahun_lahir = 2000 + thn if thn < 25 else 1900 + thn

    try:
        tanggal = datetime.date(tahun_lahir, bln, tgl_lahir)
    except:
        return {'status': 'error', 'pesan': 'Tanggal lahir tidak valid'}

    hari_ini = datetime.date.today()
    usia = hari_ini.year - tanggal.year - ((hari_ini.month, hari_ini.day) < (tanggal.month, tanggal.day))
    ultah = datetime.date(hari_ini.year, tanggal.month, tanggal.day)
    if ultah < hari_ini:
        ultah = datetime.date(hari_ini.year + 1, tanggal.month, tanggal.day)
    selisih_ultah = (ultah - hari_ini).days

    nama = NIK_TO_NAMA.get(nik, 'Tidak ditemukan')

    return {
        'status': 'success',
        'pesan': 'NIK valid',
        'data': {
            'nik': nik,
            'nama_lengkap': nama,
            'kelamin': kelamin,
            'lahir': tanggal.strftime('%d/%m/%Y'),
            'provinsi': get_nama_wilayah(PROVINSI, kode_prov, 2),
            'kotakab': get_nama_wilayah(KOTA, kode_kota, 4),
            'kecamatan': get_nama_wilayah(KEC, kode_kec, 6),
            'uniqcode': uniqcode,
            'tambahan': {
                'kodepos': KODEPOS.get(kode_kec, '-'),
                'zodiak': get_zodiac(tanggal.day, tanggal.month),
                'usia': f'{usia} tahun',
                'ultah': f'{selisih_ultah} hari lagi'
            }
        }
    }

# ------------------ ZODIAK ------------------
def get_zodiac(day, month):
    zodiacs = [
        (20, "Capricorn"), (19, "Aquarius"), (20, "Pisces"),
        (20, "Aries"), (21, "Taurus"), (21, "Gemini"),
        (23, "Cancer"), (23, "Leo"), (23, "Virgo"),
        (23, "Libra"), (22, "Scorpio"), (22, "Sagittarius")
    ]
    return zodiacs[month - 1][1] if day < zodiacs[month - 1][0] else zodiacs[month % 12][1]

# ------------------ weton ------------------
def get_weton(tanggal):
    weton = ['Legi', 'Pahing', 'Pon', 'Wage', 'Kliwon']
    base_date = dt(1900, 1, 1)
    selisih = (tanggal - base_date).days
    return weton[selisih % 5]

# ------------------ API WILAYAH ------------------
def get_wilayah(kode_prov, kode_kab, kode_kec):
    try:
        url = f"https://www.emsifa.com/api-wilayah-indonesia/api/province/{kode_prov}.json"
        prov_response = requests.get(url).json()
        prov = prov_response['name'] if 'name' in prov_response else 'Tidak ditemukan'
    except:
        prov = "-"

    try:
        kab_response = requests.get("https://www.emsifa.com/api-wilayah-indonesia/api/regencies/{}.json".format(kode_prov)).json()
        kab = next((x['name'] for x in kab_response if x['id'][2:4] == kode_kab), '-')
    except:
        kab = "-"

    try:
        kec_response = requests.get("https://www.emsifa.com/api-wilayah-indonesia/api/districts/{}.json".format(kode_kab)).json()
        kec = next((x['name'] for x in kec_response if x['id'][4:6] == kode_kec), '-')
    except:
        kec = "-"

    return f"[✔] Provinsi      : {prov}\n[✔] Kabupaten/Kota: {kab}\n[✔] Kecamatan     : {kec}"

# ------------------ CEK NOMOR HP ------------------
def cek_nomor_hp(nomor):
    try:
        if nomor.startswith("08"):
            nomor = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            nomor = "+" + nomor

        parsed = phonenumbers.parse(nomor, "ID")
        valid = phonenumbers.is_valid_number(parsed)
        carrier = phonenumbers.carrier.name_for_number(parsed, "id")
        region = phonenumbers.geocoder.description_for_number(parsed, "id")
        return f"""
[✔] Nomor Valid   : {valid}
[✔] Operator      : {carrier}
[✔] Wilayah       : {region}
"""
    except Exception as e:
        return f"Nomor tidak valid atau error: {e}"

# ------------------ CEK EMAIL ------------------
def cek_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, email):
        domain = email.split('@')[-1]
        return f"[✔] Format email valid\n[✔] Domain: {domain}"
    return "Email tidak valid."

# ------------------ CEK USERNAME ------------------
def cek_username(username):
    social_media = ["https://instagram.com/{}", "https://x.com/{}", "https://github.com/{}", "https://tiktok.com/{}", "https://threads.net/{}", "https://open.spotify.com/{}", "https://discord.com/{}", "https://web.telegram.org/{}", "https://m.facebook.com/{}", "https://snackvideo.com/{}", "https://snapchat.com/{}", "https://id.linkedin.com/{}"]
    hasil = ""
    for url in social_media:
        full_url = url.format(username)
        try:
            r = requests.get(full_url)
            status = "ADA" if r.status_code == 200 else "TIDAK ADA"
            hasil += f"[✔] {full_url} : {status}\n"
        except:
            hasil += f"[✖] {full_url} : ERROR\n"
    return hasil

# ------------------ CEK GOOGLE DORK ------------------
def google_dork(keyword):
    dorks = [
        f"site:pastebin.com {keyword}",
        f"site:github.com {keyword}",
        f"intitle:index.of {keyword}",
        f"inurl:/php?={keyword}",
        f"intext:{keyword} filetype:pdf"
    ]
    result = "\n[!] Google Dork Suggestions:\n"
    for d in dorks:
        result += f"[✔] {d}\n"
    return result

# ------------------ CEK DOMAIN / IP ------------------
def lookup_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        who = whois.whois(domain)
        return f"""
[✔] Domain : {domain}
[✔] IP     : {ip}
[✔] Registrar : {who.registrar}
[✔] Country   : {who.country}
[✔] Created   : {who.creation_date}
"""
    except:
        return "Domain/IP tidak bisa diproses."

# ------------------ HASHING TOOLS ------------------
def generate_hash(data):
    hasil = ""
    hasil += f"[✔] MD5     : {hashlib.md5(data.encode()).hexdigest()}\n"
    hasil += f"[✔] SHA1    : {hashlib.sha1(data.encode()).hexdigest()}\n"
    hasil += f"[✔] SHA256  : {hashlib.sha256(data.encode()).hexdigest()}\n"
    hasil += f"[✔] Base64  : {base64.b64encode(data.encode()).decode()}\n"
    return hasil

# ------------------ MAIN ------------------
def main():
    banner()
    print("1. Cek NIK")
    print("2. Cek Nomor HP")
    print("3. Cek Email")
    print("4. Cek Username")
    print("5. Google Dork Generator")
    print("6. Domain/IP Lookup")
    print("7. Encode (Hash/BASE64)")
    pilihan = input("\nPilih menu: ")

    if pilihan == '1':
        nik_input = input("Masukkan NIK (16 digit): ")
        print(parse_nik(nik_input))
    elif pilihan == '2':
        nomor = input("Masukkan Nomor HP (cth: 08xxxx atau +62xxxx): ")
        print(cek_nomor_hp(nomor))
    elif pilihan == '3':
        email = input("Masukkan Email: ")
        print(cek_email(email))
    elif pilihan == '4':
        user = input("Masukkan Username: ")
        print(cek_username(user))
    elif pilihan == '5':
        key = input("Masukkan keyword: ")
        print(google_dork(key))
    elif pilihan == '6':
        domain = input("Masukkan domain atau IP: ")
        print(lookup_domain(domain))
    elif pilihan == '7':
        data = input("Masukkan data untuk encode/hash: ")
        print(generate_hash(data))
    else:
        print("Pilihan tidak tersedia.")

if __name__ == '__main__':
    main()