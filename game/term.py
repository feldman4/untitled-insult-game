import json
import socket

from curtsies import FullscreenWindow, Input, FSArray
from curtsies.fmtfuncs import red, blue, bold, green, on_blue, yellow, cyan, magenta

from game.comm import connect_socket, send_start, send_string, receive_string
from game.constants import *


def init():
    model = {
        'description': 'DESCRIPTION',
        'header': 'HEADER',
        'buffer': '',
        'last': '',
        'log': '',
        'candidates': [],
        'choices': ['CHOICE_0', 'CHOICE_1'],
        'socket': None,
        'history': (-1, []),
    }
    return model


def run():
    model = init()
    history = []

    with FullscreenWindow() as window, Input() as input_generator:

        while True:
            if model['socket'] == None:
                try:
                    model['socket'] = connect_socket()
                    send_string(model['socket'], LOAD_1)
                except (socket.timeout, ConnectionRefusedError):
                    model['socket'] = None
            handle_incoming(model)
            
            old_model = model.copy()
            c = input_generator.send(TIMEOUT)
            model = handle_key(model, c)
            model = update_candidates(model)

            if model != old_model:
                history += [model]

            view(model, window)


def handle_incoming(model):
    """Read any incoming message on the socket and deal with it.
    """
    m = model
    if m['socket'] != None:
        try:
            # read from socket
            incoming = receive_string(m['socket'])
            if incoming == None or not incoming:
                return model
            message = json.loads(incoming)
            if message['kind'] == 'model_send':
                m['log'] = 'received model_send'
                return level_start(model, message['content'])
        except socket.timeout:
            pass
    return model


def level_start(model, content):
    for key in content:
        model[key] = content[key]
    return model


def handle_key(model, c):
    m = model

    if c == None:
        pass
    elif c in SYSTEM_CODES:
        send_string(m['socket'], SYSTEM_CODES[c])
    elif c == '<BACKSPACE>':
        m['buffer'] = m['buffer'][:-1]
    # if complete or uniquely autocompleted, send buffer as message to server
    elif c == '<SPACE>':
        m = update_candidates(m)
        if len(m['candidates']) == 1:
            m['buffer'] = m['candidates'][0]
        if m['buffer'] in m['choices']:
            word = m['buffer']
            m['last'] = word
            m['buffer'] = ''
            m['candidates'] = m['choices']
            send_string(m['socket'], word)
    elif any(x.lower().startswith(m['buffer'] + c.lower()) for x in m['choices']):
        m['buffer'] = (m['buffer'] + c).lower()
        m = update_candidates(m)

    return m


def send_last(model):
    m = model
    if m['socket'] != None:
        try:
            m['socket'].send(m['last'].encode())
        except socket.timeout:
            pass


def view(model, window):
    m = model
    h, w = window.height, window.width
    a = FSArray(h, w)
    with open('logs/view', 'w') as fh:
        print('model', m, file=fh)
    rows = [
        red(' '*w),
        red(' '*w),
        green(m['description']),
        cyan(m['buffer']),
        cyan('OPTIONS: ' + ' '.join(m['candidates'])),
        magenta('{header}'.format(**model)),
        # red('LOG: ' + m['log']),
    ]
    rows += [red(x) for x in format_history(m['history'])]
    rows += [blue('socket dead' if m['socket'] == None else 'socket alive'),]
    for i, row in enumerate(rows):
        # limit width to match terminal
        row = row[:w]
        a[i, :row.width] = [row]
    window.render_to_terminal(a)


def format_history(history):
    frame, timeline = history
    rows = [' --- history --- ']
    if frame == -1:
        rows += [f'FRAME: {len(timeline)}']
    else:
        rows += [f'FRAME: {frame + 1}/{len(timeline)}']

    formatted = [f'[{i}] {msg}' for i, msg in enumerate(timeline)]
    past = formatted if frame == -1 else formatted[:frame]
    future = [] if frame == -1 else formatted[frame:]

    rows += ['PAST: ' +  ' '.join(past[-3:][::-1])]
    rows += ['FUTURE: ' +  ' '.join(future[:3])]

    return rows

def update_candidates(model):
    model['candidates'] = [x for x in model['choices'] 
                           if x.lower().startswith(model['buffer'])]
    return model


if __name__ == '__main__':
    run()