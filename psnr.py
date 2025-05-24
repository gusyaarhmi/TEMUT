#!/usr/bin/env python3

import numpy as np
import cv2
import math

def calculate_mse(original_image, stego_image):
    """
    Menghitung Mean Squared Error (MSE) antara dua gambar
    
    Args:
        original_image: Gambar asli dalam bentuk array numpy
        stego_image: Gambar yang dimodifikasi dalam bentuk array numpy
    
    Returns:
        Nilai MSE (float)
    """
    # Ensure images have the same dimensions
    if original_image.shape != stego_image.shape:
        raise ValueError("Images must have the same dimensions")
    
    # Convert to float for calculation
    original = original_image.astype(np.float64)
    stego = stego_image.astype(np.float64)
    
    # Calculate MSE
    mse = np.mean((original - stego) ** 2)
    return mse

def calculate_psnr(original_image, stego_image):
    """
    Menghitung Peak Signal-to-Noise Ratio (PSNR) antara dua gambar
    
    Args:
        original_image: Gambar asli dalam bentuk array numpy
        stego_image: Gambar yang dimodifikasi dalam bentuk array numpy
    
    Returns:
        Nilai PSNR dalam dB (float)
    """
    mse = calculate_mse(original_image, stego_image)
    
    # Menangani kasus jika gambar identik
    if mse == 0:
        return float('inf')
    
    # Asumsi gambar 8-bit (nilai maksimum 255)
    max_pixel = 255.0
    
    # Menghitung PSNR
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr

if __name__ == "__main__":
    # Contoh
    original = cv2.imread('original.png')
    stego = cv2.imread('stego.png')
    
    if original is not None and stego is not None:
        psnr_value = calculate_psnr(original, stego)
        print(f"PSNR: {psnr_value:.2f} dB")
    else:
        print("Error loading images")