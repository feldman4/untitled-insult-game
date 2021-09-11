import socket

from curtsies import FullscreenWindow, Input, FSArray
from curtsies.fmtfuncs import red, blue, bold, green, on_blue, yellow

from game.constants import PORT, TIMEOUT
from game.comm import connect_socket


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
                except socket.timeout:
                    model['socket'] = None
            if model['socket'] != None:
                try:
                    # read from socket
                    incoming = model['socket'].recv(1024).decode()
                    if incoming:
                        model['log'] += ' | ' + incoming
                except socket.timeout:
                    pass
                
            
            old_model = model.copy()
            c = input_generator.send(1)
            model = handle_key(model, c)
            model = update_candidates(model)

            if model != old_model:
                history += [model]

            view(model, window)


def handle_key(model, c):
    m = model
    if c == None:
        return model

    if any(x.startswith(m['buffer'] + c) for x in m['allowed']):
        m['buffer'] += c

    m = update_candidates(m)

    if c == '<SPACE>':
        if len(m['candidates']) == 1:
            m['buffer'] = m['candidates'][0]
        if m['buffer'] in m['allowed']:
            m['last'] = m['buffer']
            m['buffer'] = ''
            m['candidates'] = m['allowed']
    return m


def view(model, window):
    m = model
    a = FSArray(window.height, window.width)
    first_row = red('{header} {last}'.format(**model))
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