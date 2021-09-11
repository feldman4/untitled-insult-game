import json
import re

def load_world(name='test'):
    with open(f'DF/twine/{name}.json', 'r') as fh:
        return parse_world(json.load(fh))

def get_enemy(passage):
    pat = 'enemy:(\w+)'
    matches = re.findall(pat, passage['text'])
    if len(matches) == 0:
        return None
    else:
        return matches[0]
    
def get_header(passage):
    return passage['text'].split('\n')[0]

def parse_world(world):
    d = {}
    for passage in world['passages']:
        level = {
            'header': get_header(passage),
        }

        links = passage['links']
        enemy = get_enemy(passage)
        if enemy != None:
            level['enemy'] = enemy
        
        if len(links) > 0:
            level['choice'] = [x['text'] for x in links]
        d[passage['name']] = level
    return d
    


example_world = dict(
vestibule = {
    'header': 'Choose your destiny',
    'choices': ['A: fight moron', 'B: fight asshole'],
},
level_1 = {
    'header': 'THE MORON: drool runs equally out both sides of his mouth', 
    'enemy': 'moron',
},
level_2 = {
    'header': 'THE ASSHOLE: his Boxter is parked on your front lawn', 
    'enemy': 'asshole',
},
hell = {
    'header': 'You died. This is mute hell.',
    'choices': [],
},
)