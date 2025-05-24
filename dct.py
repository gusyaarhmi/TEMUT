#!/usr/bin/env python3

import cv2
import numpy as np

class AppError(BaseException):
  pass

def i2bin(i, l):
  actual = bin(i)[2:]
  if len(actual) > l:
    raise AppError("bit size is larger than expected.")

  while len(actual) < l:
    actual = "0"+actual

  return actual

def char2bin(c):
  return i2bin(ord(c), 8)

# DCT digunakan untuk melakukan manipulasi gambar terutama penyisipan pesan rahasia menggunakan metode DCT (Discrete Cosine Transform)
class dct_steg():

 # sebelum menyisipkan pesan rahasia pada gambar, kita perlu mengetahui sel mana yang digunakan atau akan digunakan untuk menyimpan pesan rahasia, untuk mencapainya, kita akan menggunakan 16 sel pertama untuk menyimpan panjang, nilai ini akan dikonversi ke biner dan tidak lebih dari 16 bit yang berarti panjang pesan maksimum adalah 2^16 = 65536
  MAX_BIT_LENGTH = 16
  # Ukuran blok DCT
  BLOCK_SIZE = 8
  # Faktor kuantisasi untuk koefisien DCT
  QUANT_FACTOR = 25
  # Koefisien mana di blok DCT yang akan dimodifikasi (menghindari koefisien DC dan komponen frekuensi rendah)
  COEFF_INDEX = 5

  def __init__(self, img):
    self.size_x, self.size_y, self.size_channel = img.shape

    self.image = img.astype(np.float32)
    # pointer yang digunakan untuk merujuk blok DCT mana pada gambar yang akan dibaca atau ditulis
    self.cur_x = 0
    self.cur_y = 0
    self.cur_channel = 0
    # Jumlah total blok dalam arah x dan y
    self.blocks_x = self.size_x // self.BLOCK_SIZE
    self.blocks_y = self.size_y // self.BLOCK_SIZE
    # Indeks blok saat ini
    self.block_idx = 0

  # pindahkan penunjuk ke blok berikutnya
  def next(self):
    self.block_idx += 1
    
    if self.cur_channel != self.size_channel-1:
      self.cur_channel += 1
    else:
      self.cur_channel = 0
      self.cur_y += self.BLOCK_SIZE
      if self.cur_y >= self.size_y - self.BLOCK_SIZE:
        self.cur_y = 0
        self.cur_x += self.BLOCK_SIZE
        if self.cur_x >= self.size_x - self.BLOCK_SIZE:
          raise AppError("need larger image")

  # Terapkan DCT ke blok saat ini
  def get_dct_block(self):
    block = self.image[self.cur_x:self.cur_x+self.BLOCK_SIZE, 
                       self.cur_y:self.cur_y+self.BLOCK_SIZE, 
                       self.cur_channel]
    return cv2.dct(block)

  # Terapkan DCT terbalik dan perbarui blok gambar
  def update_block(self, dct_block):
    idct_block = cv2.idct(dct_block)
    self.image[self.cur_x:self.cur_x+self.BLOCK_SIZE, 
               self.cur_y:self.cur_y+self.BLOCK_SIZE, 
               self.cur_channel] = idct_block

  # masukkan satu bit ke koefisien DCT
  def put_bit(self, bit):
    dct_block = self.get_dct_block()
    
    # Dapatkan koefisien frekuensi tengah (5,5)
    coeff = dct_block[self.COEFF_INDEX, self.COEFF_INDEX]
    
    # Koefisien kuantisasi
    quant_coeff = round(coeff / self.QUANT_FACTOR)
    
    # Ubah koefisien menjadi genap atau ganjil berdasarkan bit
    if bit == '0' and quant_coeff % 2 == 1:
      quant_coeff -= 1
    elif bit == '1' and quant_coeff % 2 == 0:
      quant_coeff += 1
    
    # Perbarui koefisien
    dct_block[self.COEFF_INDEX, self.COEFF_INDEX] = quant_coeff * self.QUANT_FACTOR
    
    # Perbarui blok pada gambar
    self.update_block(dct_block)
    
    # Pindah ke blok berikutnya
    self.next()

  # put_bits meletakkan array bit ke blok yang ditunjuk masing-masing
  def put_bits(self, bits):
    for bit in bits:
      self.put_bit(bit)

  # read_bit membaca bit tertanam dari koefisien DCT
  def read_bit(self):
    dct_block = self.get_dct_block()
    
    # Dapatkan koefisien frekuensi tengah
    coeff = dct_block[self.COEFF_INDEX, self.COEFF_INDEX]
    
    # Koefisien kuantisasi
    quant_coeff = round(coeff / self.QUANT_FACTOR)
    
    # Koefisien genap mengkodekan '0', koefisien ganjil mengkodekan '1'
    bit = '1' if quant_coeff % 2 == 1 else '0'
    
    # Pindah ke blok berikutnya
    self.next()
    
    return bit

  # read_bits membaca bit tertanam dari blok DCT
  def read_bits(self, length):
    bits = ""
    for _ in range(0, length):
      bits += self.read_bit()

    return bits

  # menyematkan teks ke gambar menggunakan DCT
  def embed(self, text):
    # Hitung panjang teks dan ubah ke biner dengan panjang 16 bit
    text_length = i2bin(len(text), self.MAX_BIT_LENGTH)
    
    # Berikan panjang pada 16 blok pertama
    self.put_bits(text_length)

    # Letakkan setiap karakter pada teks ke gambar
    for c in text:
      # Konversi karakter menjadi biner dengan panjang 8
      bits = char2bin(c)
      # Taruh setiap bit ke dalam blok masing-masing
      self.put_bits(bits)
    
    # Konversi kembali ke uint8 untuk penyimpanan yang tepat
    self.image = np.clip(self.image, 0, 255).astype(np.uint8)

  # mengekstrak teks dari gambar menggunakan DCT
  def extract(self):
    # Baca 16 blok pertama sepanjang teks yang terdapat pada gambar
    length = int(self.read_bits(self.MAX_BIT_LENGTH), 2)
    text = ""
    for _ in range(0, length):
      # Baca setiap 8 bit sebagai karakter
      c = int(self.read_bits(8), 2)
      # Konversi biner menjadi karakter
      text += chr(c)

    return text

  # simpan gambar ke dstPath
  def save(self, dstPath):
    # Pastikan gambar dalam format uint8 sebelum menyimpan
    image_to_save = np.clip(self.image, 0, 255).astype(np.uint8)
    cv2.imwrite(dstPath, image_to_save)

if __name__ == "__main__":
    # obj = dct_steg(cv2.imread('src.jpg')) 
    # obj.embed("ku yakin pasti suatu saat semua mungkin terjadi, kau kan mencintaiku dan tak akan pernah melepasku aku mau mendampingi dirimu, aku mau mencintai kekuranganmu, s'lalu bersedia bahagiakanmu apapun yang terjadi, kujanjikan aku ada...") 
    # obj.simpan('dst.png')

  obj = dct_steg(cv2.imread('dst.png'))
  text = obj.extract()
  print(text)