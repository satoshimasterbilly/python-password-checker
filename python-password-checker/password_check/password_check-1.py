"""PasswordChecker Project
"""
import sys
import hashlib
import getpass

import requests


def main(*plain_passwords, obscured=True):
    """"""
    for plain_password in plain_passwords:
        check_password(plain_password, obscured=bool(obscured))


def get_api_response(hashed_password):
    try:
        hash_prefix = hashed_password[:5]
        api_url = 'https://api.pwnedpasswords.com/range/' + hash_prefix
        response = requests.get(api_url)
        if not response.status_code == 200:
            raise RuntimeError(
                f'Invalid query "{hash_prefix}", please try again.')
        return response
    except RuntimeError as e:
        raise e


def get_leaked_password_hashes(api_response):
    """Return list with tuples containing leaked hash and leaks count.

    Arguments:
        api_response - requests.response object
    Return:
        ordered iterable

    Api response is a string separated with a delimiter for each hash
     item.  The actual hash tail consists of the first 35 characters.
    Thereafter the count is separated by a colon (:).  The remaining
     chars after the colon is the number of times the password has been
     leaked.
    """
    delimiter, end_of_hash, start_of_count = '\r\n', 35, 36
    return [(hash_data[:end_of_hash], int(hash_data[start_of_count:]))
            for hash_data in api_response.text.split(delimiter)]


def get_password_leaks_count(hashed_password, hashes):
    """Return number of times password has been leaked."""
    try:
        if len(hashed_password) > 35:
            hashed_password = hashed_password[5:]  # Check hash tail
        index = [hashed[0] for hashed in hashes].index(hashed_password)
        return hashes[index][1]  # Leaks
    except (IndexError, ValueError):
        return 0  # No leaks


def get_password_sha1_hashes(plain_password):
    """Return tuple with hashed password prefix and tail."""
    hashed_password = hashlib.sha1(
        plain_password.encode('utf-8')).hexdigest().upper()
    return hashed_password[:5], hashed_password[5:]


def pwned_api_check(plain_password):
    """Return number of times password has been leaked."""
    hashed_prefix, hashed_tail = get_password_sha1_hashes(plain_password)
    response = get_api_response(hashed_prefix)
    leaked_hashes = get_leaked_password_hashes(response)
    return get_password_leaks_count(hashed_tail, leaked_hashes)


def check_password(plain_password, obscured=True):
    """Print message with number of times password has been leaked."""
    times_leaked = pwned_api_check(plain_password)
    password_output = obscure(plain_password) if obscured else plain_password
    if times_leaked:
        print(f'Your password {password_output} has been leaked '
              f"{times_leaked} time{'' if times_leaked == 1 else 's'}!")
    else:
        print(f'Password {password_output} has not been leaked!')


def obscure(plain_password):
    """Replace every second character in password with *."""
    return ''.join(f'{char}*' for char in plain_password[:-1:2]) \
           + plain_password[-1]


if __name__ == '__main__':
    try:
        password = sys.argv[1:]
        if not password:
            raise ValueError('Password cannot be empty.')
    except (IndexError, ValueError):
        while True:
            password = getpass.getpass('Password to check: ')
            if password:
                main(password)
                check_again = input(
                    'Do you want to check another password? Y/n ')
                if check_again.lower() in ('y', 'yes'):
                    continue
                break
            print('Please enter a password string.')
    else:
        sys.exit(main(*password, obscured=False))
        # Todo: Ability to print plain text password after security
        #  warning, instead of pseudo encrypting.
        # Todo: Add passwords to check into txt file via terminal and then
        #  run for all.
