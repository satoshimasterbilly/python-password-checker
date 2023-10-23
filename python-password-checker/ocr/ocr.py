from PIL import Image
import pytesseract


def generate_passwords(image_names):
    """Generate passwords from image names."""
    passwords = []
    for image_name in image_names:
        text_output = get_string_from_image(image_name)
        passwords_from_image = [
            password for password in get_generated_passwords(text_output)
            if password not in passwords]
        passwords.extend(passwords_from_image)
    return passwords


def get_string_from_image(image_name):
    """Return string of text in image."""
    try:
        return pytesseract.image_to_string(Image.open(image_name))
    except IOError:
        return ''


def get_generated_passwords(text_output):
    """Filter text output and return generator containing passwords."""
    newline,  = '\n'
    text_output = text_output.replace(' ', '')  # Remove any blank space
    passwords = text_output.split(newline)  # Split outside loop
    passwords = (password.strip() for password in passwords if password)
    return passwords


def get_passwords(text_output):
    """Return generated passwords."""
    return list(get_generated_passwords(text_output))


if __name__ == '__main__':
    pass
