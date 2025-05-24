#!/usr/bin/env python3
import cv2
import numpy as np
import os
from dct import dct_steg
from aes import AESCipher

class RobustnessTest:
    def __init__(self, original_image, encoded_image, cipher_text, key):
        """
        Inisialisasi pengujian robustness dengan data yang diperlukan
        
        Parameter:
        original_image -- Gambar asli (numpy array)
        encoded_image -- Gambar hasil steganografi (numpy array)
        cipher_text -- Teks terenkripsi yang disisipkan ke dalam gambar
        key -- Kunci enkripsi AES
        """
        self.original_image = original_image
        self.encoded_image = encoded_image
        self.cipher_text = cipher_text
        self.key = key
        self.cipher = AESCipher(key)
        
    def _extract_and_compare(self, attacked_image):
        """
        Extract   Ekstrak pesan dari gambar yang telah diserang dan bandingkan dengan pesan asli
        
        Returns:
        success -- Boolean indicating if extraction was successful
        decoded_message -- Extracted message (if successful)
        error -- Error message (if not successful)
        """
        try:
            obj = dct_steg(attacked_image)
            extracted_cipher = obj.extract()
            
            # Decrypt the message
            decrypted_message = self.cipher.decrypt(extracted_cipher)
            decoded_message = decrypted_message.decode('utf-8').rstrip()
            
            # If we get here, extraction was successful
            return True, decoded_message, None
        except Exception as e:
            return False, None, str(e)
    
    def resize_test(self, factors):
        """
        Test robustness against image resizing
        
        Parameters:
        factors -- List of resize factors (e.g., [0.5, 0.75, 1.25, 1.5])
        
        Returns:
        results -- Dictionary with test results
        """
        results = {}
        
        for factor in factors:
            height, width = self.encoded_image.shape[:2]
            new_height = int(height * factor)
            new_width = int(width * factor)
            
            # Resize down
            resized_down = cv2.resize(self.encoded_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            # Resize back to original
            resized_back = cv2.resize(resized_down, (width, height), interpolation=cv2.INTER_CUBIC)
            
            success, message, error = self._extract_and_compare(resized_back)
            
            results[factor] = {
                'success': success,
                'message': message if success else None,
                'error': error if not success else None,
                'resized_image': resized_back
            }
        
        return results
    
    def noise_test(self, noise_type, params):
        """
        Uji robustness terhadap noise
        
        Parameter:
        noise_type -- Jenis noise: 'gaussian' atau 'salt_pepper'
        params -- 
            Untuk gaussian: list standar deviasi
            Untuk salt_pepper: list densitas noise
        
        Return:
        results -- Dictionary berisi hasil uji
        """
        results = {}
        
        
        for param in params:
            noisy_image = self.encoded_image.copy()
            
            if noise_type == 'gaussian':
                # Tambahkan Gaussian noise
                mean = 0
                stddev = param
                noise = np.random.normal(mean, stddev, noisy_image.shape).astype(np.float32)
                noisy_image = noisy_image.astype(np.float32) + noise
                noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
            
            elif noise_type == 'salt_pepper':
                # Tambahkan Salt and Pepper noise
                density = param
                salt_mask = np.random.rand(*noisy_image.shape[:2]) < (density / 2)
                pepper_mask = np.random.rand(*noisy_image.shape[:2]) < (density / 2)
                
                # Terapkan salt
                noisy_image[salt_mask] = 255
                # Terapkan pepper
                noisy_image[pepper_mask] = 0

            else:
                results[param] = {
                    'success': False,
                    'message': None,
                    'error': f"Unknown noise type: {noise_type}",
                    'noisy_image': noisy_image
                }
                continue
            
            success, message, error = self._extract_and_compare(noisy_image)
            
            results[param] = {
                'success': success,
                'message': message if success else None,
                'error': error if not success else None,
                'noisy_image': noisy_image
            }
        
        return results
    
    def jpeg_compression_test(self, qualities):
        """
        Uji robustness terhadap kompresi JPEG
        
        Parameter:
        qualities -- List nilai kualitas JPEG (0-100)
        
        Return:
        results -- Dictionary berisi hasil uji
        """
        results = {}
        
        for quality in qualities:
            temp_jpg = "temp_compressed.jpg"
            
            # Simpan gambar dengan kualitas tertentu
            cv2.imwrite(temp_jpg, self.encoded_image, [cv2.IMWRITE_JPEG_QUALITY, quality])
            
            # Baca kembali gambar yang dikompresi
            compressed_image = cv2.imread(temp_jpg)
            
            if os.path.exists(temp_jpg):
                os.remove(temp_jpg)
            
            success, message, error = self._extract_and_compare(compressed_image)
            
            results[quality] = {
                'success': success,
                'message': message if success else None,
                'error': error if not success else None,
                'compressed_image': compressed_image
            }
        
        return results
