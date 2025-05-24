#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from psnr import calculate_psnr
from ssim import calculate_ssim

class StegoAnalyzer:
    """
    Kelas untuk menganalisis dan membandingkan metode steganografi
    """
    
    def __init__(self):
        """Inisialisasi penganalisa"""
        self.results = {}
        
    def add_result(self, method_name, original_image, stego_image, message_length=0):
        """
        Tambahkan hasil steganografi untuk dianalisis

        Argumen:
        method_name: Nama metode steganografi
        original_image: Gambar asli sebagai array numpy atau jalur ke gambar
        stego_image: Gambar stego sebagai array numpy atau jalur ke gambar
        message_length: Panjang pesan tersembunyi dalam byte
        """
        # Load images if paths are provided
        if isinstance(original_image, str):
            original_image = cv2.imread(original_image)
        
        if isinstance(stego_image, str):
            stego_image = cv2.imread(stego_image)
        
        # Calculate PSNR
        psnr_value = calculate_psnr(original_image, stego_image)
        
        # Store result
        self.results[method_name] = {
            'psnr': psnr_value,
            'message_length': message_length,
            'original_image': original_image,
            'stego_image': stego_image
        }
        
    def print_comparison(self):
        """Print perbandingan semua metode"""
        if not self.results:
            print("No results to compare.")
            return
        
        print("\n===== Steganography Methods Comparison =====")
        print(f"{'Method':<20} {'PSNR (dB)':<12} {'SSIM':<10} {'Message Length':<15}")
        print("-" * 60)

        for method, result in self.results.items():
            print(f"{method:<20} {result['psnr']:<12.2f} {result['ssim']:<10.4f} {result['message_length']:<15}")

    
    def plot_comparison(self, save_path=None):
        """
        Plot perbandingan nilai PSNR untuk metode yang berbeda
        
        Argumen:
        save_path: Jalur untuk menyimpan plot (opsional)
        """
        if not self.results:
            print("No results to plot.")
            return
        
        methods = list(self.results.keys())
        psnr_values = [self.results[method]['psnr'] for method in methods]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(methods, psnr_values, color='skyblue')
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.2f} dB',
                    ha='center', va='bottom', rotation=0)
        
        plt.xlabel('Steganography Method')
        plt.ylabel('PSNR (dB)')
        plt.title('Comparison of Steganography Methods by PSNR')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add a horizontal line indicating good quality threshold
        plt.axhline(y=30, color='r', linestyle='--', alpha=0.5)
        plt.text(0, 30.5, 'Good Quality Threshold (30 dB)', color='r')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def generate_report(self, output_path="stego_analysis_report.html"):
        """
        Hasilkan laporan HTML yang membandingkan metode

        Argumen:
        jalur_output: Jalur untuk menyimpan laporan HTML
        """
        if not self.results:
            print("No results to generate report.")
            return
        
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Steganography Analysis Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2 { color: #333; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .good { color: green; }
                .average { color: orange; }
                .poor { color: red; }
            </style>
        </head>
        <body>
            <h1>Steganography Analysis Report</h1>
            <h2>PSNR Comparison</h2>
            <table>
                <tr>
                    <th>Method</th>
                    <th>PSNR (dB)</th>
                    <th>Quality Assessment</th>
                    <th>Message Length</th>
                </tr>
        """
        
        for method, result in self.results.items():
            psnr = result['psnr']
            
            # Determine quality class
            if psnr > 40:
                quality_class = "good"
                quality_text = "Excellent"
            elif psnr > 30:
                quality_class = "good"
                quality_text = "Good"
            elif psnr > 20:
                quality_class = "average"
                quality_text = "Acceptable"
            else:
                quality_class = "poor"
                quality_text = "Poor"
            
            html_content += f"""
                <tr>
                    <td>{method}</td>
                    <td>{psnr:.2f}</td>
                    <td class="{quality_class}">{quality_text}</td>
                    <td>{result['message_length']} bytes</td>
                </tr>
            """
        
        html_content += """
            </table>
            <h2>Interpretation</h2>
            <ul>
                <li><strong>Excellent (PSNR > 40 dB):</strong> Changes are imperceptible</li>
                <li><strong>Good (PSNR > 30 dB):</strong> Changes might be visible under close inspection</li>
                <li><strong>Acceptable (PSNR > 20 dB):</strong> Changes may be noticeable</li>
                <li><strong>Poor (PSNR ≤ 20 dB):</strong> Changes are clearly visible</li>
            </ul>
            <p>Generated on: <script>document.write(new Date().toLocaleString())</script></p>
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f"Report generated and saved to {output_path}")

def add_result(self, method_name, original_image, stego_image, message_length=0):
    """
    Tambahkan hasil steganografi untuk dianalisis

    Argumen:
    method_name: Nama metode steganografi
    original_image: Gambar asli sebagai array numpy atau jalur ke gambar
    stego_image: Gambar stego sebagai array numpy atau jalur ke gambar
    message_length: Panjang pesan tersembunyi dalam byte
    """
    if isinstance(original_image, str):
        original_image = cv2.imread(original_image)

    if isinstance(stego_image, str):
        stego_image = cv2.imread(stego_image)

    psnr_value = calculate_psnr(original_image, stego_image)
    ssim_value = calculate_ssim(original_image, stego_image)

    self.results[method_name] = {
        'psnr': psnr_value,
        'ssim': ssim_value,
        'message_length': message_length,
        'original_image': original_image,
        'stego_image': stego_image
    }
