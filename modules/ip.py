import whois

def lookup_ip(domain):
    try:
        data = whois.whois(domain)
        return str(data)
    except Exception as e:
        return f"[!] Gagal lookup: {e}"
