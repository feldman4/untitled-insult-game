import socket

from game.constants import PORT, TIMEOUT

def connect_socket():
    client = socket.socket()
    address=("localhost", PORT)
    client.settimeout(TIMEOUT)
    client.connect(address)
    return client

