import socket
import json

from game.constants import *
from game.comm import send_string

def setup():
    server = socket.socket()
    server.bind(('localhost',PORT))   # takes a tuple
    server.settimeout(TIMEOUT)
    server.listen(5) # up to 5 connections...
    return server


def run():
    server = setup()
    clients = []
    while True:
        try:
            client, addr = server.accept()
            print('Got connection from', addr)
            client.settimeout(TIMEOUT)
            clients = [client]
        except socket.timeout:
            pass
        
        # listen for message
        if len(clients) == 0:
            continue
        this_client = clients[0]
        try:
            incoming = this_client.recv(1024).decode()
            if incoming:
                print('Heard', incoming)
            if incoming == START:
                send_start_state(this_client)

        except socket.timeout:
            pass


level_1 = ('Type your shit!!!', ['apostate', 'apiculturist', 'bandito'])


def send_start_state(client):
    msg = level_start(*level_1)
    send_string(client, msg)
    print(msg)


def level_start(header, allowed):
    return json.dumps({
        'kind': 'level_start',
        'content': {
            'header': header,
            'allowed': allowed,
        }
    })