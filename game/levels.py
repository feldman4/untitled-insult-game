import json
import re
import xmltodict
from natsort import natsorted
from glob import glob


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
    
def get_description(passage):
    return passage['text'].split('\n')[0]

def parse_world(world):
    d = {}
    for passage in world['passages']:
        level = {
            'description': get_description(passage),
        }

        links = passage['links']
        enemy = get_enemy(passage)
        if enemy != None:
            level['enemy'] = enemy
        
        if len(links) > 0:
            level['choices'] = [(x['text'], x['destination']['name']) for x in links]
        d[passage['name']] = level
    return d


def extract_links(txt):
    capture = '\[\[(.*)->(.*)\]\]'
    match = '\[\[.*->.*\]\]'
    matches = re.findall(capture, txt)
    matches
    for x in re.findall(match, txt):
        txt = txt.replace(x, '')
    txt = txt.strip()
    return txt, matches


def load_passage(passage_data):
    cleaned, links = extract_links(passage_data['#text'])
    level = {
        'description': cleaned,
        'links': links, 
        'tags': parse_tags(passage_data['@tags']),
    }
    return level

def parse_tags(txt):
    pat = '(\w+):(\w+)'
    return dict(re.findall(pat, txt))

def load_world(story):
    return {x['@name']: load_passage(x) 
            for x in story['tw-passagedata']}


def load_archive(filename, verbose=False):
    """Load a Twine archive from https://twinery.org/2
    """
    # make it xml
    with open(filename, 'r') as fh:
        txt = fh.read()
    txt = txt.replace('hidden>', '>')
    txt = f'<archive>{txt}</archive>'
    archive = xmltodict.parse(txt)
    archive = json.loads(json.dumps(archive))
    archive = archive['archive']['tw-storydata']
    if not isinstance(archive, list):
        archive = [archive]
    return archive


def load_worlds(search, verbose=True):
    """Parse Twine archives into worlds. Archive files are sorted, and later 
    archives overwrite earlier ones.
    """
    files = natsorted(glob(search))
    worlds = {}
    for f in files:
        archive = load_archive(f, verbose=verbose)
        for story in archive:
            worlds[story['@name']] = load_world(story)
    return {k: worlds[k] for k in sorted(worlds)}