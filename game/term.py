import json
import socket

from curtsies import FullscreenWindow, Input, FSArray
from curtsies.fmtfuncs import red, blue, bold, green, on_blue, yellow

from game.comm import connect_socket, send_start, send_string

def init():
    model = {
        'header': 'Type your shit:',
        'buffer': '',
        'last': '',
        'log': '',
        'candidates': [],
        'allowed': ['apple', 'appman', 'banana'],
        'socket': None,
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
                except (socket.timeout, ConnectionRefusedError):
                    model['socket'] = None
            handle_incoming(model)
            
            old_model = model.copy()
            c = input_generator.send(1)
            model = handle_key(model, c)
            model = update_candidates(model)

            if model != old_model:
                history += [model]

            view(model, window)


def handle_incoming(model):
    if model['socket'] != None:
        try:
            # read from socket
            incoming = model['socket'].recv(1000000).decode()
            if not incoming:
                return model
            message = json.loads(incoming)
            if message['kind'] == 'level_start':
                model['log'] = 'received level_start'
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
        return model

    if any(x.startswith(m['buffer'] + c) for x in m['allowed']):
        m['buffer'] += c

    m = update_candidates(m)

    # special start string
    if c == '1':
        send_start(m['socket'])

    if c == '<SPACE>':
        if len(m['candidates']) == 1:
            m['buffer'] = m['candidates'][0]
        if m['buffer'] in m['allowed']:
            word = m['buffer']
            m['last'] = word
            m['buffer'] = ''
            m['candidates'] = m['allowed']
            send_string(m['socket'], word)

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
    a = FSArray(window.height, window.width)
    first_row = red('{header}'.format(**model))
    second_row = blue(m['buffer'])
    third_row = green(' '.join(m['candidates']))
    fourth_row = red('LOG: ' + m['log'])
    if m['socket'] == None:
        fifth_row = blue('socket dead')
    else:
        fifth_row = blue('socket alive')

    a[0, :first_row.width] = [first_row]
    a[1, :second_row.width] = [second_row]
    a[2, :third_row.width] = [third_row]
    a[3, :fourth_row.width] = [fourth_row]
    a[4, :fifth_row.width] = [fifth_row]
    window.render_to_terminal(a)


def update_candidates(model):
    model['candidates'] = [x for x in model['allowed'] 
                           if x.startswith(model['buffer'])]
    return model


if __name__ == '__main__':
    run()