import socket as socket_lib

from game.constants import *


def connect_socket():
    client = socket_lib.socket()
    address = ("localhost", PORT)
    client.settimeout(TIMEOUT)
    client.connect(address)
    return client


def send_string(socket, s):
    if socket is None:
        return
    try:
        socket.send(s.encode())
    except socket_lib.timeout:
        pass


def send_start(socket):
    send_string(socket, START)


def receive_string(socket):
    try:
        incoming = socket.recv(100000).decode()
        return incoming
    except (socket_lib.timeout, ConnectionResetError):
        return None


def get_new_client(server):
    try:
        client, addr = server.accept()
        print('Got connection from', addr)
        client.settimeout(TIMEOUT)
        return client
    except socket_lib.timeout:
        return None


def create_server():
    server = socket_lib.socket()
    server.setsockopt(socket_lib.SOL_SOCKET, socket_lib.SO_REUSEADDR, 1)
    server.setsockopt(socket_lib.SOL_SOCKET, socket_lib.SO_REUSEPORT, 1)
    server.bind(('localhost',PORT))   # takes a tuple
    server.settimeout(TIMEOUT)
    server.listen(5) # up to 5 connections...
    return server
