import socket
import json
import sys
import datetime

from game.constants import *
from game.comm import send_string, receive_string, get_new_client, create_server
from game.actors import Player, Enemy
from game.levels import load_world, load_worlds

"""
socket problems
- other stuff
"""


enemies = {
    'moron': lambda: Enemy(hp=20, xp=10, weakness='intelligence'),
    'asshole': lambda: Enemy(hp=20, xp=10, weakness='intelligence'),
}


def print(*args, file=sys.stderr, **kwargs):
    import builtins
    builtins.print(*args, file=file, **kwargs)


def init(client, world):
    import random
    random.seed(0)
    player = Player(hp=30, weakness='weight')
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
        'history': (-1, []),
    }
    return model


# the server model is indexed by the client ID
def run():
    worlds = load_worlds(TWINE_ARCHIVE)
    first_world = list(worlds.values())[0]

    server = create_server()
    model = None
    while True:
        new_client = get_new_client(server)
        if new_client != None:
            model = init(new_client, first_world)
        if model == None:
            continue
        
        # listen for message
        message = receive_string(model['client'])
        if message:
            print(f'RECEIVE: {message}')
            model = handle_message(model, message)
            send_model(model)


# model -> message -> model
def handle_message(model, message):
    m = model
    if message in SYSTEM_CODES.values():
        model = handle_special_code(model, message)
    elif model['player'].current_enemy == None:
        model = handle_choice(model, message)
    else:
        model = handle_repartee(model, message)
    model = update_history(model, message)
    return model


def update_history(model, message):
    """If frame is -1, add any message other than time ones. Else add nothing.
    """
    if message in (REWIND, FFORWARD, SYNCHRONIZE):
        pass
    else:
        frame, timeline = model['history']
        if frame == -1:
            model['history'] = frame, timeline + [message]
    return model


def handle_special_code(model, message):
    m = model
    # START THE GAME
    if message in LOAD_SIGNALS:
        i = LOAD_SIGNALS.index(message)
        worlds = load_worlds(TWINE_ARCHIVE)
        name, world = list(worlds.items())[i]
        model = init(m['client'], world)
        transition(m, m['level'])
        print(f'{message}: Loaded {name}')
    if message == REWIND:
        frame, timeline = model['history']
        if frame == -1:
            frame = len(timeline)
        frame = max(0, frame - 1)
        model['history'] = (frame, timeline)
        model = play_to_frame(model)
    if message == FFORWARD:
        frame, timeline = model['history']
        if frame != -1:
            frame = min(len(timeline) - 1, frame + 1)
            model['history'] = (frame, timeline)
            model = play_to_frame(model)
    if message == SYNCHRONIZE:
        frame, timeline = model['history']
        model['history'] = (-1, timeline[:frame])
        model = play_to_frame(model)

    return model


def play_to_frame(model):
    m = model
    frame, timeline = m['history']
    new_model = init(m['client'], m['world'])
    for message in timeline[:frame]:
        new_model = handle_message(new_model, message)
    new_model['history'] = frame, timeline
    return new_model


def handle_choice(model, message):
    m = model
    link_map = dict(m['world'][m['level']]['links'])
    if message in link_map and link_map[message] in m['world']:
        transition(model, link_map[message])
    else:
        print('Transition not recognized', message)
    return model


def handle_repartee(model, message):
    print('Entering repartee')
    m = model
    enemy = m['player'].current_enemy
    first_hp = enemy.hp
    enemy.take_mental_damage(message)
    print(f'Player insults with "{message}": enemy HP {first_hp}=>{enemy.hp}')
    
    if enemy.hp <= 0:
        # victory
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
            m['player'].current_enemy = None
            transition(model, 'hell')
            m['status'] = 'Death.'
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
    if 'enemy' in level['tags']:
        enemy_name = level['tags']['enemy']
        # create the enemy
        enemy = enemies[enemy_name]()
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
    content = {
        'header': format_header(model),
        'description': m['world'][m['level']]['description'],
        'history': m['history'],
    }
    
    # determine user's text choices
    level = m['world'][m['level']]
    if m['player'].current_enemy == None:
        content['choices'] = [x[0] for x in level['links']]
    else:
        content['choices'] = model['player'].vocabulary

    msg = json.dumps({
        'kind': 'model_send',
        'content': content,
    })
    send_string(model['client'], msg)

    log(content, 'model_send')
    log(copy_without(model, 'client'), 'model')


def log(value, label, file=sys.stdout):
    timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print(f'### {timestamp}: {label}', file=file, flush=True)
    print(value, file=file, flush=True)


def copy_without(d, *keys):
    import copy
    d = {k: d[k] for k in d if k not in keys}
    return copy.deepcopy(d)
