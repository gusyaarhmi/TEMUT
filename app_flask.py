#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename
from dct import dct_steg
from aes import AESCipher
from psnr import calculate_psnr
from ssim import calculate_ssim
from robustness import RobustnessTest

app = Flask(__name__)
app.secret_key = "temut_secret_key"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Buat folder unggah jika belum ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'robustness'), exist_ok=True)

# Variabel global untuk menyimpan data sementara
temp_image = None
temp_original_image = None  # Menyimpan gambar asli untuk perhitungan PSNR
temp_output_path = None
temp_cipher_text = None  # Menyimpan cipher text untuk robustness test

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global temp_image, temp_original_image

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Baca gambar langsung dari objek file
        file_bytes = file.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Simpan gambar asli untuk perhitungan PSNR dan SSIM nanti
        temp_original_image = img.copy()

        # Simpan gambar dalam memori
        temp_image = img

        # Simpan file sementara
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'wb') as f:
            f.write(file_bytes)

        original_filename = "original_image.png"
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        cv2.imwrite(original_path, img)  # menyimpan gambar asli

        flash('Image successfully uploaded')
        return render_template('index.html', image_uploaded=True, image_path=filepath)

    flash('Invalid file type. Please upload an image file.')
    return redirect(request.url)

@app.route('/encode', methods=['POST'])
def encode():
    global temp_image, temp_original_image, temp_output_path, temp_cipher_text

    if temp_image is None:
        flash('Please upload an image first')
        return redirect(url_for('index'))

    key = request.form.get('key', '')
    message = request.form.get('message', '')

    if len(key) != 16:
        flash('Key must be 16 characters')
        return redirect(url_for('index'))

    if len(message) % 16 != 0:
        message += (" " * (16 - len(message) % 16))

    try:
        # Enkripsi pesan
        cipher = AESCipher(key)
        cipher_text = cipher.encrypt(message)
        
        # Simpan cipher_text untuk pengujian ketahanan
        temp_cipher_text = cipher_text

        # Sisipkan ke gambar
        obj = dct_steg(temp_image)
        obj.embed(cipher_text)
        result_image = obj.image

        # Hitung PSNR dan SSIM
        psnr_value = calculate_psnr(temp_original_image, result_image)
        ssim_value = calculate_ssim(temp_original_image, result_image)

        # Simpan hasil encode
        output_filename = "encoded_image.png"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        cv2.imwrite(output_path, result_image)
        temp_output_path = output_path
        
        # Update temp_image untuk operasi decode
        temp_image = result_image

        flash(f'Message encoded successfully. PSNR: {psnr_value:.2f} dB, SSIM: {ssim_value:.4f}')
        return render_template('index.html',
                               image_uploaded=True,
                               encoded=True,
                               psnr_value=f"{psnr_value:.2f}",
                               ssim_value=f"{ssim_value:.4f}",
                               image_path=url_for('static', filename='uploads/encoded_image.png'),
                               original_path=url_for('static', filename='uploads/original_image.png'))

    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/decode', methods=['POST'])
def decode():
    global temp_image

    if temp_image is None:
        flash('Please upload an image first')
        return redirect(url_for('index'))

    key = request.form.get('key', '')

    if len(key) != 16:
        flash('Key must be 16 characters')
        return redirect(url_for('index'))

    try:
        obj = dct_steg(temp_image)
        cipher_text = obj.extract()

        cipher = AESCipher(key)
        decrypted_message = cipher.decrypt(cipher_text)

        decoded_message = decrypted_message.decode('utf-8').rstrip()

        flash('Message decoded successfully')
        return render_template('index.html',
                               image_uploaded=True,
                               decoded=True,
                               decoded_message=decoded_message,
                               image_path=request.form.get('current_image'))

    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/download')
def download():
    global temp_output_path

    if temp_output_path and os.path.exists(temp_output_path):
        return send_file(temp_output_path, as_attachment=True)

    flash('No encoded image available for download')
    return redirect(url_for('index'))

@app.route('/test_robustness', methods=['POST'])
def test_robustness():
    global temp_image, temp_original_image, temp_cipher_text
    
    if temp_image is None or temp_cipher_text is None:
        flash('Please encode a message first before testing robustness')
        return redirect(url_for('index'))
    
    key = request.form.get('robustness_key', '')
    test_type = request.form.get('test_type', '')
    
    if len(key) != 16:
        flash('Key must be 16 characters')
        return redirect(url_for('index'))
    
    # Inisialisasi uji ketahanan
    robustness = RobustnessTest(temp_original_image, temp_image, temp_cipher_text, key)
    
    results_data = {}
    test_results = []
    
    try:
        # Lakukan tes yang dipilih
        if test_type == 'resize':
            factors = [0.5, 0.75, 0.9, 1.1, 1.25, 1.5]
            results = robustness.resize_test(factors)
            
            for factor, result in results.items():
                # Simpan gambar yang diserang
                img_filename = f"resize_{factor}.png"
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'robustness', img_filename)
                cv2.imwrite(img_path, result['resized_image'])
                
                relative_path = f"uploads/robustness/{img_filename}"
                
                test_results.append({
                    'type': 'Resize',
                    'param': f"{factor}x",
                    'success': result['success'],
                    'message': result['message'] if result['success'] else result['error'],
                    'image_path': relative_path
                })
        
        elif test_type == 'gaussian':
            stddevs = [5, 10, 15, 20, 25]
            results = robustness.noise_test('gaussian', stddevs)
            
            for stddev, result in results.items():
                # Simpan gambar yang diserang
                img_filename = f"gaussian_{stddev}.png"
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'robustness', img_filename)
                cv2.imwrite(img_path, result['noisy_image'])
                
                relative_path = f"uploads/robustness/{img_filename}"
                
                test_results.append({
                    'type': 'Gaussian Noise',
                    'param': f"σ={stddev}",
                    'success': result['success'],
                    'message': result['message'] if result['success'] else result['error'],
                    'image_path': relative_path
                })
        
        elif test_type == 'salt_pepper':
            densities = [0.01, 0.02, 0.05, 0.1, 0.15]
            results = robustness.noise_test('salt_pepper', densities)
            
            for density, result in results.items():
                # Simpan gambar yang diserang
                img_filename = f"salt_pepper_{int(density*100)}.png"
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'robustness', img_filename)
                cv2.imwrite(img_path, result['noisy_image'])
                
                relative_path = f"uploads/robustness/{img_filename}"
                
                test_results.append({
                    'type': 'Salt & Pepper Noise',
                    'param': f"{density*100}%",
                    'success': result['success'],
                    'message': result['message'] if result['success'] else result['error'],
                    'image_path': relative_path
                })
        
        elif test_type == 'jpeg':
            qualities = [100, 90, 80, 70, 60, 50, 40, 30]
            results = robustness.jpeg_compression_test(qualities)
            
            for quality, result in results.items():
                # Simpan gambar yang diserang
                img_filename = f"jpeg_{quality}.png"
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'robustness', img_filename)
                cv2.imwrite(img_path, result['compressed_image'])
                
                relative_path = f"uploads/robustness/{img_filename}"
                
                test_results.append({
                    'type': 'JPEG Compression',
                    'param': f"Quality {quality}",
                    'success': result['success'],
                    'message': result['message'] if result['success'] else result['error'],
                    'image_path': relative_path
                })
        
        # Hitung tes yang berhasil
        successful_tests = sum(1 for result in test_results if result['success'])
        total_tests = len(test_results)
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        flash(f'Robustness test completed. Success rate: {success_rate:.1f}% ({successful_tests}/{total_tests})')
        
        return render_template('index.html',
                              image_uploaded=True,
                              robustness_tested=True,
                              test_results=test_results,
                              test_type=test_type,
                              success_rate=f"{success_rate:.1f}%",
                              image_path=url_for('static', filename='uploads/encoded_image.png'))
    
    except Exception as e:
        flash(f'Error during robustness testing: {str(e)}')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)