# Panduan Instalasi Aplikasi Steganografi DCT

## Persyaratan Sistem
- Python 3.7 atau versi yang lebih baru
- pip (Python package installer)

## Langkah-langkah Instalasi

### 1. Clone atau Download Proyek
```bash
# Jika menggunakan git
git clone <url-repository>
cd steganografi-dct

# Atau download dan ekstrak file ZIP
```

### 2. Buat Virtual Environment (Disarankan)
```bash
# Membuat virtual environment
python -m venv venv

# Mengaktifkan virtual environment
# Untuk Windows:
venv\Scripts\activate

# Untuk Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install semua package yang diperlukan
pip install -r requirements.txt
```

### 4. Verifikasi Instalasi
```bash
# Jalankan script untuk memeriksa semua dependency
python check_dependencies.py
```

### 5. Jalankan Aplikasi
```bash
# Menjalankan aplikasi Flask
python app_flask.py
```

Aplikasi akan berjalan di `http://localhost:5000` atau `http://127.0.0.1:5000`

## Troubleshooting

### Jika terjadi error saat instalasi opencv-python:
```bash
# Coba install versi yang lebih kecil
pip install opencv-python-headless==4.8.1.78
```

### Jika terjadi error dengan scikit-image:
```bash
# Install dependency tambahan untuk Windows
pip install --upgrade setuptools wheel
pip install scikit-image --no-cache-dir
```

### Jika terjadi error dengan pycryptodome:
```bash
# Untuk Windows, mungkin perlu Microsoft Visual C++ Build Tools
# Atau coba install versi pre-compiled:
pip install --only-binary=all pycryptodome
```

## Penggunaan Aplikasi

1. **Upload Gambar**: Pilih gambar yang akan digunakan untuk menyembunyikan pesan
2. **Encode Pesan**: 
   - Masukkan kunci enkripsi (harus 16 karakter)
   - Masukkan pesan yang akan disembunyikan
   - Klik "Encode Message"
3. **Decode Pesan**:
   - Masukkan kunci yang sama
   - Klik "Decode Message"
4. **Test Robustness**: Uji ketahanan pesan terhadap berbagai serangan

## Fitur Utama

- **Steganografi DCT**: Menyembunyikan pesan menggunakan Discrete Cosine Transform
- **Enkripsi AES**: Pesan dienkripsi sebelum disembunyikan
- **Analisis Kualitas**: Menghitung PSNR dan SSIM
- **Uji Ketahanan**: Test terhadap resize, noise, dan kompresi JPEG
- **Interface Web**: Antarmuka yang mudah digunakan

## Struktur File Proyek

```
steganografi-dct/
├── app_flask.py          # Aplikasi web Flask utama
├── dct.py               # Implementasi steganografi DCT
├── aes.py               # Enkripsi AES
├── psnr.py              # Perhitungan PSNR
├── ssim.py              # Perhitungan SSIM
├── robustness.py        # Uji ketahanan
├── requirements.txt     # Daftar dependency
├── check_dependencies.py # Script verifikasi instalasi
├── templates/           # Template HTML
├── static/             # File CSS dan gambar
└── static/uploads/     # Folder untuk file upload
```