def generate_dorks(keyword):
    dorks = [
        f'site:facebook.com "{keyword}"',
        f'site:linkedin.com "{keyword}"',
        f'site:tokopedia.com "{keyword}"',
        f'site:pastebin.com "{keyword}"'
    ]
    return "\n".join(dorks)
