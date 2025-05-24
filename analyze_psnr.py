#!/usr/bin/env python3

import cv2
import argparse
import os
from psnr import calculate_psnr, calculate_mse

def analyze_image_quality(original_path, stego_path):
    """
    Menganalisis kualitas citra antara gambar asli dan gambar stego
    
    Args:
        original_path: Path ke gambar asli
        stego_path: Path ke gambar stego
    """
    # Membaca image
    original = cv2.imread(original_path)
    stego = cv2.imread(stego_path)
    
    if original is None:
        print(f"Error: Could not load original image from {original_path}")
        return
    
    if stego is None:
        print(f"Error: Could not load stego image from {stego_path}")
        return
    
    # Memeriksa apakah kedua gambar memiliki dimensi yang sama
    if original.shape != stego.shape:
        print(f"Error: Images have different dimensions: {original.shape} vs {stego.shape}")
        return
    
    # Menghitung nilai MSE dan PSNR
    mse = calculate_mse(original, stego)
    psnr = calculate_psnr(original, stego)
    
    # Menampilkan hasil analisis
    print("\n====== Image Quality Analysis ======")
    print(f"Original Image: {os.path.basename(original_path)}")
    print(f"Stego Image: {os.path.basename(stego_path)}")
    print(f"Mean Squared Error (MSE): {mse:.6f}")
    print(f"Peak Signal-to-Noise Ratio (PSNR): {psnr:.2f} dB")
    print("===================================")
    
    # Interpretation
    if psnr > 40:
        print("Interpretation: Excellent quality. The changes are imperceptible.")
    elif psnr > 30:
        print("Interpretation: Good quality. Changes might be visible under close inspection.")
    elif psnr > 20:
        print("Interpretation: Acceptable quality. Changes may be noticeable.")
    else:
        print("Interpretation: Poor quality. Changes are clearly visible.")

def main():
    parser = argparse.ArgumentParser(description="Analyze image quality between original and stego images")
    parser.add_argument("original", help="Path to the original image")
    parser.add_argument("stego", help="Path to the stego image")
    
    args = parser.parse_args()
    analyze_image_quality(args.original, args.stego)

if __name__ == "__main__":
    main()