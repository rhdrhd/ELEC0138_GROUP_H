import requests

ip = "127.0.0.1"
port = 15000
pack = 1000
num_threads = 1000
num_requests = 10000
api_suffix = "/api/v1/venues"


def socket_send():
    import random
    import socket

    hh = random._urandom(10)
    xx = 0
    while True:
        try:
            # Correct syntax for creating a socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the server
            s.connect((ip, port))

            s.send(hh)

            for i in range(pack):
                s.send(hh)

            xx += 1
            print(f"Attack {ip} | Sent: {xx}")
        except Exception as e:
            s.close()
            print(e)


def main(num_threads, option):
    from concurrent.futures import ThreadPoolExecutor, as_completed

    try:
        func = options[option]
    except:
        raise Exception(
            f"Unsupported option: {option}! All available options: {options.keys()}"
        )

    success = 0
    futures = []
    # Using ThreadPoolExecutor to manage threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Map the function to an iterable of arguments
        for _ in range(num_requests):
            futures.append(executor.submit(func))
    for future in as_completed(futures, timeout=100):
        try:
            res = future.result()
        except Exception as e:
            raise e
        else:
            if res:
                success += 1
    print(f"{success=} {num_requests=} Success Rate: {success/num_requests}")


def http_get():

    resp = requests.get(f"http://{ip}:{port}{api_suffix}")
    return True if resp.status_code == 200 else False


options = {
    "socket": socket_send,
    "http": http_get,
}

if __name__ == "__main__":
    import sys

    assert len(sys.argv) > 1, f"Please choose your option: {', '.join(options.keys())}"
    option = sys.argv[1]
    main(num_threads=num_threads, option=option)
