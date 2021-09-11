import socket
import json

from game.constants import *
from game.comm import send_string, receive_string, get_new_client, create_server

"""
socket problems
- killing server kills the port
- other stuff
"""


vestibule = {
    'header': 'Choose your destiny',
    'allowed': ['A: fight moron', 'B: fight asshole']
}
level_1 = {
    'header': 'THE MORON: drool runs equally out both sides of his mouth', 
    'allowed': ['apostate', 'apiculturist', 'bandito'],
}
level_2 = {
    'header': 'THE ASSHOLE: his Boxter is parked on your front lawn', 
    'allowed': ['pedo', 'loser'],
}

links = {
    'A: fight moron': level_1,
    'B: fight asshole': level_2,
    }

def send_start_state(client):
    print('Sending start')
    send_string(client, level_start(vestibule))


# the server model is indexed by the client ID
def run():
    server = create_server()
    models = []
    i = 0
    while True:
        new_client = get_new_client(server)
        if new_client != None:
            models += [{'level': vestibule, 'client': new_client}]

        # listen for message
        for i, m in enumerate(models):
            message = receive_string(m['client'])
            if message:
                print(f'Heard {message} from client {i}')
                models[i] = handle_message(m, message)


def handle_message(model, message):
    m = model
    # START THE GAME
    if message == START:
        send_start_state(m['client'])
    # TRANSITION ROOMS
    elif message in links:
        transition(model, links[message])
        print(f'Transition {message} to {links[message]}')
    # AN INSULT CAME IN
    return m


def transition(model, level):
    msg = level_start(level)
    send_string(model['client'], msg)


def level_start(level):
    return json.dumps({
        'kind': 'level_start',
        'content': level,
    })


