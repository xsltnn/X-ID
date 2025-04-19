import dns.resolver

def validate_email(email):
    domain = email.split('@')[-1]
    try:
        mx = dns.resolver.resolve(domain, 'MX')
        return f"[✔] Email domain valid: {domain}"
    except:
        return f"[✖] Email domain tidak valid: {domain}"
