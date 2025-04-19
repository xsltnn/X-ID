def parse_nik(nik):
    if len(nik) != 16 or not nik.isdigit():
        return "[✖] Format NIK tidak valid"
    return f"[✔] NIK valid: {nik}"
