import socket
import json

from game.constants import *
from game.comm import send_string, receive_string, get_new_client, create_server
from game.actors import Player, Enemy

"""
socket problems
- killing server kills the port
- other stuff
"""


vestibule = {
    'header': 'Choose your destiny',
    'choices': ['A: fight moron', 'B: fight asshole']
}
level_1 = {
    'header': 'THE MORON: drool runs equally out both sides of his mouth', 
    'enemy': 'moron',
}
level_2 = {
    'header': 'THE ASSHOLE: his Boxter is parked on your front lawn', 
    'enemy': 'asshole',
}
hell = {
    'header': 'You died. This is mute hell.',
    'choices': [],
}

enemies = {
    'moron': Enemy(hp=3, xp=10, weakness='intelligence'),
    'asshole': Enemy(hp=3, xp=10, weakness='intelligence'),
}

links = {
    'A: fight moron': level_1,
    'B: fight asshole': level_2,
    }


def init(client):
    player = Player(hp=40, weakness='weight')
    player.vocabulary = ['idiot', 'fatso', 'streber', 'moron', 'chucklehead']
    model = {
        'level': vestibule, 
        'client': client, 
        'player': player,
    }
    return model


# the server model is indexed by the client ID
def run():
    server = create_server()
    models = []
    i = 0
    while True:
        new_client = get_new_client(server)
        if new_client != None:
            models += [init(new_client)]

        # listen for message
        for i, m in enumerate(models):
            message = receive_string(m['client'])
            if message:
                print(f'Heard {message} from client {i}')
                models[i] = handle_message(m, message)


# model -> message -> model
def handle_message(model, message):
    m = model
    # START THE GAME
    if message == START:
        print('START TRANSITION')
        transition(model, level_1)
    # TRANSITION ROOMS
    elif message in links:
        transition(model, links[message])
    # AN INSULT CAME IN
    else:
        m = model
        enemy = m['player'].current_enemy
        print('Player insults with:', message)
        enemy.take_mental_damage2(message)
        if enemy.hp <= 0:
            # victory
            m['player'].xp += enemy.xp
            m['player'].current_enemy = None
            transition(m, vestibule)
        else:
            enemy_insult, enemy_response = enemy.respond()
            m['player'].take_mental_damage(enemy_response)
            if m['player'].hp <= 0:
                transition(model, hell)
            else:
                # hack to show enemy insult
                m['level']['header'] = f'HP: {m["player"].hp}; Enemy says {enemy_insult}'
                level_send(model)
    return m


def transition(model, level):
    """Transition the model to the level, then send the level to the front end.
    """
    model['level'] = level
    print('Transitioning to', level)
    if 'enemy' in level:
        enemy = enemies[level['enemy']]
        model['player'].current_enemy = enemy
    level_send(model)


def level_send(model):
    """Send level info to the front end.
    """
    level = model['level']
    content = {'header': level['header']}
    if 'choices' in level:
        content['choices'] = level['choices']
    else:
        content['choices'] = model['player'].vocabulary
    msg = json.dumps({
        'kind': 'level_start',
        'content': content,
    })
    send_string(model['client'], msg)
    print('sent', msg)
    


