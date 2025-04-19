def cek_marketplace(username):
    platforms = ['tokopedia.com', 'bukalapak.com', 'shopee.co.id']
    hasil = [f"https://www.{p}/@{username}" for p in platforms]
    return "\n".join(hasil)
