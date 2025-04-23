# MOO T2 V5 - OSINT Tool Indonesia 🇮🇩
# Created by XSLTNN
# Powerful OSINT Tools for Indonesia - All-in-One Terminal Toolkit

import requests
import re
import os
import db
import socket
from db import search_by_name, search_by_phone, search_by_email
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

          MASSIVE OSINT OPERATION TARGET 2
 Created by XSLTNN - Powerful Indonesian OSINT Toolkit (V5)
''')

# ------------------ CEK NIK ------------------
def parse_nik(nik):
    if len(nik) != 16 or not nik.isdigit():
        return "NIK tidak valid (harus 16 digit angka)."

    kode_prov = nik[:2]
    kode_kab = nik[2:4]
    kode_kec = nik[4:6]
    tanggal = int(nik[6:8])
    bulan = int(nik[8:10])
    tahun = int(nik[10:12])

    kelamin = "Perempuan" if tanggal > 40 else "Laki-laki"
    tanggal_lahir = tanggal - 40 if kelamin == "Perempuan" else tanggal

    now_year = int(dt.now().strftime("%y"))
    tahun_lahir = 1900 + tahun if tahun > now_year else 2000 + tahun
    usia = dt.now().year - tahun_lahir

    ultah = dt(tahun_lahir, bulan, tanggal_lahir).strftime("%d %B %Y")

    zodiak = get_zodiac(tanggal_lahir, bulan)
    weton = get_weton(dt(tahun_lahir, bulan, tanggal_lahir))

    wilayah = get_wilayah(kode_prov, kode_kab, kode_kec)

    return f"""
[✔] Jenis Kelamin : {kelamin}
[✔] Tanggal Lahir : {ultah}
[✔] Usia          : {usia} tahun
[✔] Zodiak        : {zodiak}
[✔] Weton         : {weton}
{wilayah}    """

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

# ------------------ MAIN ------------------
def main():
    banner()

    print("1. Cari NIK")
    print("2. Cari berdasarkan Nama")
    print("3. Cari berdasarkan Nomor Telepon")
    print("4. Cari berdasarkan Email")
    pilihan = input("\nPilih menu: ")

    if pilihan == '1':
        nik_input = input("Masukkan NIK (16 digit): ")
        print(parse_nik(nik_input))

    elif pilihan == '2':
        name = input("Masukkan Nama: ")
        results = search_by_name(name)
        print_results(results)

    elif pilihan == '3':
        phone = input("Masukkan Nomor Telepon: ")
        results = search_by_phone(phone)
        print_results(results)

    elif pilihan == '4':
        email = input("Masukkan Email: ")
        results = search_by_email(email)
        print_results(results)

def print_results(results):
    if results:
        for r in results:
            print("─" * 50)
            print(f"[Collection: {r.get('_collection')}] Matched on: {r.get('_matched_field')}")
            for key, val in r.items():
                if not key.startswith("_"):
                    print(f"{key}: {val}")
    else:
        print("❌ Data tidak ditemukan.")

# Cek apakah file ini dijalankan langsung
if __name__ == '__main__':
    main()
