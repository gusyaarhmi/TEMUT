#!/usr/bin/env python3

from Crypto.Cipher import AES

class AESCipher:
    """
    Kelas AESCipher untuk enkripsi/dekripsi teks menggunakan algoritma AES
    Ketentuan:
    - panjang key: harus 16 karakter
    - panjang pesan: harus kelipatan 16
    """
    
    def __init__(self, key):
        """Inisialisasi cipher dengan key enkripsi"""
        self.key = key.encode('utf-8')
    
    def encrypt(self, msg):
        """
        Mengenkripsi pesan menggunakan key
        Argumen:
            msg: pesan teks biasa yang akan dienkripsi
        Mengembalikan:
            String heksadesimal dari data terenkripsi
        """
        # Membuat objek AES cipher baru dalam mode ECB
        aes_instance = AES.new(self.key, AES.MODE_ECB)
        
        # Melakukan enkripsi dan mengubah hasilnya ke heksadesimal
        encrypted_data = aes_instance.encrypt(msg.encode('utf-8'))
        return encrypted_data.hex()
    
    def decrypt(self, cipherText):
        """
        Mendekripsi ciphertext menggunakan key
        Argumen:
            cipherText: string heksadesimal dari data terenkripsi
        Mengembalikan:
            Pesan hasil dekripsi dalam bentuk byte
        """
        # Membuat objek AES cipher baru dalam mode ECB untuk dekripsi
        aes_instance = AES.new(self.key, AES.MODE_ECB)
        
        # Mengubah hex ke byte lalu melakukan dekripsi
        return aes_instance.decrypt(bytes.fromhex(cipherText))


# Contoh penggunaan saat script dijalankan langsung
if __name__ == "__main__":
    # Menguji implementasi
    cipher = AESCipher("temutsangatimutz")
    
    # Pesan asli
    original_message = "SepertiItulah"
    print(f"Original: {original_message}")
    
    # Mengenkripsi pesan
    encrypted = cipher.encrypt(original_message)
    print(f"Encrypted: {encrypted}")
    
    # Mendekripsi pesan
    decrypted = cipher.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")