# ssim.py

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def calculate_ssim(original_image, stego_image):
    """
    Hitung Indeks Kesamaan Struktural (SSIM) antara dua gambar.

    Argumen:
    original_image (numpy.ndarray): Gambar asli.
    stego_image (numpy.ndarray): Gambar stego (yang dimodifikasi).

    Pengembalian:
    float: Nilai SSIM antara -1 dan 1
    """
    # Convert to grayscale
    original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    stego_gray = cv2.cvtColor(stego_image, cv2.COLOR_BGR2GRAY)

    # Hitung SSIM
    ssim_value, _ = ssim(original_gray, stego_gray, full=True)
    return ssim_value
