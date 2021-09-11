import socket
import json

from game.constants import *
from game.comm import send_string, receive_string, get_new_client, create_server
from game.actors import Player, Enemy
from game.levels import example_world

"""
socket problems
- killing server kills the port
- other stuff
"""


enemies = {
    'moron': Enemy(hp=3, xp=10, weakness='intelligence'),
    'asshole': Enemy(hp=3, xp=10, weakness='intelligence'),
}

def init(client, world=example_world):
    player = Player(hp=40, weakness='weight')
    player.vocabulary = ['idiot', 'fatso', 'streber', 
                         'moron', 'chucklehead']
    first_level = list(world.values())[0]['name']
    model = {
        'client': client, 
        'player': player,
        'world': world,
        'level': first_level, # start on first level
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
    elif message in m['world']:
        transition(model, message)
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
            first_level = list(worlds.values())[0]
            transition(m, first_level)
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


def transition(model, level_name):
    """Transition the model to the level, then send the 
    level to the front end.
    """
    m = model
    m['level'] = level_name
    level = m['world'][level_name]
    print('Transitioning to', level_name)
    if 'enemy' in level:
        enemy = enemies[level['enemy']]
        m['player'].current_enemy = enemy
    level_send(model)


def level_send(model):
    """Send level info to the front end.
    """
    m = model
    level = m['world'][m['level']]
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

