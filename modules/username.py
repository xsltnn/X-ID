def cek_username(username):
    sites = [
        f"https://instagram.com/{username}",
        f"https://twitter.com/{username}",
        f"https://github.com/{username}",
        f"https://facebook.com/{username}"
    ]
    return "\n".join(sites)
