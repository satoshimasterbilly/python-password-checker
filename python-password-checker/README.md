# PasswordChecker
### Reading passwords from images and checking for leaks

### Installation
1. Install the dependencies
    ```
    $ pip install -r requirements.txt
    ```

2. Run and pass image directory as parameter using either relative or absolute path
    ![Sample image](/../master/sample_img/sample.png?raw=true "Sample passwords to check")
    
    The sample dir `sample_img` contains only one image, `sample.png`, resulting in the below output:
    ```
    $ python -m main sample_img
    Your password J*s*i*a*2 has been leaked 33 times!y
    Your password secret123 has been leaked 17080 times!
    Your password hello has been leaked 253581 times!
    Password W*l*e*i*e*8*6 has not been leaked!
    ```
    To "obscure" the output, set `obscured` to `True` for `main` (`main(IMAGE_NAMES, obscured=True)`) in `main.py`:
    ```
    Your password p*s*w*r*d has been leaked 3730471 times!
    Your password p*s*w*r*1*3 has been leaked 251686 times!
    Your password 
    Password P*S*W*j has not been leaked!
    ```
   Note that white space is intentionally stripped from both input and output when reading passwords from an image.

### Dependencies
* [python >= 3.7](https://www.python.org/downloads/) (Not tested with lower versions but will require at least 3.6 due to f-strings)
* [requests](https://pypi.org/project/requests/) - Requests
* [Pillow](https://pypi.org/project/Pillow/) - Pillow
* [pytesseract](https://pypi.org/project/pytesseract/) - Python-tesseract


### Attributions
* Using [Pwned Passwords API](https://haveibeenpwned.com/API/v3#PwnedPasswords) to check passwords
* Based on a project in the course [Complete Python Developer in 2020: Zero to Mastery](https://www.udemy.com/share/101URoAkofdl9UQXw=/)
    
    The course teaches how to use the Pwned Passwords API to check if a password has been leaked. The code in this project is mainly my implementation and extension of the course project. I then added the read from image feature and have plans to improve it further by using a custom trained model.