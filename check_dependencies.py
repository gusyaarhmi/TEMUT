from flask import Flask

def check_flask_version():
    flask_version = Flask.__version__
    print(f"Flask version: {flask_version}")
    return flask_version

if __name__ == "__main__":
    try:
        import cv2
        cv2_version = cv2.__version__
        print(f"OpenCV version: {cv2_version}")
    except ImportError:
        print("OpenCV not installed. Please install it with: pip install opencv-python")
    
    try:
        import numpy as np
        numpy_version = np.__version__
        print(f"NumPy version: {numpy_version}")
    except ImportError:
        print("NumPy not installed. Please install it with: pip install numpy")
    
    try:
        from PIL import Image, __version__ as pillow_version
        print(f"Pillow version: {pillow_version}")
    except ImportError:
        print("Pillow not installed. Please install it with: pip install pillow")
    
    try:
        from Crypto.Cipher import AES
        from Crypto import __version__ as crypto_version
        print(f"PyCryptodome version: {crypto_version}")
    except ImportError:
        print("PyCryptodome not installed. Please install it with: pip install pycryptodome")
    
    flask_version = check_flask_version()
    
    print("\nAll dependencies checked. You can now run the application with:")
    print("python app_flask.py")