# MOO T2 V5 - OSINT Tool Indonesia 🇮🇩

**Powerful Terminal-based OSINT Tool untuk investigasi data Indonesia.**  
Fitur utama: deteksi data dari NIK, pencarian nama, email, dan nomor telepon.

---

## 🚀 Fitur

- 🔍 Cek informasi NIK (zodiak, weton, usia, kelamin, lokasi)
- 📡 Pencarian Nama
- 📧 Pencarian Email
- 📞 Pencarian Nomor Telepon

---

## ⚙️ Cara Install & Jalankan

### 1. Clone & install dependensi
```bash
git clone https://github.com/xsltnn/x-id.git
cd x-id
pip install -r requirements.txt
```

### 2. Buat file `.env`
Isi dengan lisensi yang kamu beli:

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

### 3. Jalankan Tool
```bash
python main.py
```

---

## 🛡️ Keamanan
- File `.env` berisi kredensial tidak diupload ke GitHub
- Gunakan `.gitignore` untuk mengabaikan file sensitif

---

## 📜 Lisensi

MIT License — by [XSLTNN]