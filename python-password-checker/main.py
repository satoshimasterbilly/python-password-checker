"""PasswordChecker Project
"""
import sys
from pathlib import Path

from ocr import ocr
from password_check import password_check as check


def main(image_names, obscured=True):
    """Get passwords from images and check each for leaks."""
    for password in ocr.generate_passwords(image_names):
        check.check_password(password, obscured)


if __name__ == '__main__':
    try:
        IMAGE_DIR_NAME = sys.argv[1]
    except IndexError:
        IMAGE_DIR_NAME = 'sample_img'

    IMAGES = Path(IMAGE_DIR_NAME).glob('*')
    IMAGE_NAMES = (str(img.joinpath()) for img in IMAGES)
    main(IMAGE_NAMES, obscured=False)
