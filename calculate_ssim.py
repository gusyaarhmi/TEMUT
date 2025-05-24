from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np

def calculate_ssim(original_image, stego_image):
    """
     Menghitung Structural Similarity Index (SSIM) antara dua gambar
    
    Args:
        original_image: Gambar asli dalam bentuk array numpy
        stego_image: Gambar stego dalam bentuk array numpy

    Returns:
        Nilai SSIM (float antara -1 sampai 1)
    """
    # Pastikan dalam format grayscale
    original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    stego_gray = cv2.cvtColor(stego_image, cv2.COLOR_BGR2GRAY)

    ssim_index, _ = ssim(original_gray, stego_gray, full=True)
    return ssim_index