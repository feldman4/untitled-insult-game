import socket

from game.constants import *

def connect_socket():
    client = socket.socket()
    address=("localhost", PORT)
    client.settimeout(TIMEOUT)
    client.connect(address)
    return client


def send_string(socket, s):
    if socket == None:
        return
    try:
        socket.send(s.encode())
    except socket.timeout:
        pass


def send_start(socket):
    send_string(socket, START)