#!/usr/bin/env python3

import os

def create_directory_structure():
    """Buat struktur direktori yang diperlukan untuk aplikasi."""
    directories = ['static', 'static/uploads', 'templates']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def check_requirements():
    """Periksa apakah paket yang diperlukan sudah terinstal."""
    try:
        import flask
        import cv2
        import numpy
        import PIL
        import werkzeug
        from Crypto.Cipher import AES
        print("All required packages are installed.")
        return True
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please install the required packages using pip:")
        print("pip install flask opencv-python numpy pillow pycryptodome")
        return False

def check_files():
    """Periksa apakah file yang diperlukan ada."""
    required_files = {
        'app_flask.py': 'Main Flask application',
        'aes.py': 'AES encryption/decryption module',
        'dct.py': 'DCT steganography module',
        'static/style.css': 'CSS styles for the web interface',
        'templates/index.html': 'HTML template for the web interface'
    }
    
    all_exists = True
    for file, description in required_files.items():
        if not os.path.exists(file):
            print(f"Missing file: {file} - {description}")
            all_exists = False
    
    if all_exists:
        print("All required files are present.")
    return all_exists

def setup():
    """Siapkan aplikasinya."""
    print("Setting up TEMUT Application...")
    create_directory_structure()
    
    requirements_ok = check_requirements()
    files_ok = check_files()
    
    if requirements_ok and files_ok:
        print("\nSetup complete! You can now run the application with:")
        print("python app_flask.py")
        print("\nThe web interface will be available at: http://127.0.0.1:5000/")
    else:
        print("\nSetup incomplete. Please resolve the issues above before running the application.")

if __name__ == "__main__":
    setup()