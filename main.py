
# main.py
import os
import sys

from modules import nomor, ip, email, marketplace, kendaraan, nama

def banner():
    print("""
╔══════════════════════════════════╗
║          X-ID v5 Toolkit         ║
║      by XSLTNN | OSINT Legal     ║
╚══════════════════════════════════╝
""")

def menu():
    print("""
[1] Cek Nomor HP
[2] IP Lookup
[3] Cek Email Breach
[4] Cek Akun Marketplace
[5] Cek Kendaraan
[6] Cek Nama Lengkap
[0] Keluar
""")

def main():
    banner()
    while True:
        menu()
        pilih = input(">>> Pilih menu: ")
        
        if pilih == "1":
            no = input("Masukkan nomor HP: ")
            print(nomor.lookup_nomor(no))

        elif pilih == "2":
            ip_input = input("Masukkan IP: ")
            print(ip.lookup_ip(ip_input))

        elif pilih == "3":
            email_input = input("Masukkan email: ")
            print(email.check_breach(email_input))

        elif pilih == "4":
            username = input("Masukkan username: ")
            print(marketplace.search_marketplace(username))

        elif pilih == "5":
            plat = input("Masukkan plat nomor: ")
            print(kendaraan.lookup_kendaraan(plat))

        elif pilih == "6":
            nama_input = input("Masukkan nama lengkap: ")
            print(nama.cari_nama(nama_input))

        elif pilih == "0":
            print("Keluar...")
            sys.exit()

        else:
            print("Pilihan tidak tersedia!")

if __name__ == "__main__":
    main()
