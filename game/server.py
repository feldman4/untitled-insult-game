import socket
import json

from game.constants import *
from game.comm import send_string, receive_string, get_new_client, create_server
from game.actors import Player, Enemy
from game.levels import load_world

"""
socket problems
- killing server kills the port
- other stuff
"""


enemies = {
    'moron': Enemy(hp=20, xp=10, weakness='intelligence'),
    'asshole': Enemy(hp=20, xp=10, weakness='intelligence'),
}

def init(client):
    world = load_world()
    player = Player(hp=40, weakness='weight')
    # should be a column from the vocab sheet
    player.vocabulary = ['idiot', 'fatso', 'streber', 
                         'moron']
    first_level = list(world)[0]
    model = {
        'client': client, 
        'player': player,
        'world': world,
        'level': first_level, # start on first level
        'status': '<init>',
    }
    return model


# the server model is indexed by the client ID
def run():
    server = create_server()
    models = []
    while True:
        new_client = get_new_client(server)
        if new_client != None:
            models += [init(new_client)]

        # listen for message
        for i, m in enumerate(models):
            message = receive_string(m['client'])
            if message:
                print(f'RECEIVE ({i}): {message}')
                models[i] = handle_message(m, message)
                send_model(models[i])


# model -> message -> model
def handle_message(model, message):
    m = model
    # START THE GAME
    if message == START:
        print('START TRANSITION')
        m['status'] = 'started'
        transition(model, 'basement')
    # TRANSITION ROOMS
    elif message in m['world']:
        transition(model, message)
    # AN INSULT CAME IN
    else:
        m = model
        enemy = m['player'].current_enemy
        first_hp = enemy.hp
        enemy.take_mental_damage(message)
        print(f'Player insults with {message}: enemy HP {first_hp}=>{enemy.hp}')
        # victory
        if enemy.hp <= 0:
            m['player'].xp += enemy.xp
            m['player'].current_enemy = None
            first_level = list(m['world'])[0]
            m['status'] = 'Victory!'
            transition(m, first_level)
        else:
            # death
            enemy_insult = enemy.respond()
            m['player'].take_mental_damage(enemy_insult)
            if m['player'].hp <= 0:
                transition(model, hell)
            else:
                # hack to show enemy insult
                m['status'] = f'Enemy says {enemy_insult}'
                
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


def format_header(model):
    m = model
    info = {
        'LEVEL': m['level'],
        'STATUS': m['status'], 
        'PLAYER HP': m['player'].hp,
    }

    enemy = m['player'].current_enemy
    if enemy != None:
        info['ENEMY HP'] = enemy.hp
        
    return ' | '.join([f'{k}={v}' for k,v in info.items()])


def send_model(model):
    """Send info to the front end.
    """
    m = model
    content = {'header': format_header(model)}
    
    # determine user's text choices
    level = m['world'][m['level']]
    if 'choices' in level:
        content['choices'] = level['choices']
    else:
        content['choices'] = model['player'].vocabulary

    msg = json.dumps({
        'kind': 'model_send',
        'content': content,
    })
    send_string(model['client'], msg)

