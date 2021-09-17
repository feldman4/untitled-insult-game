import json
import socket
import re

from curtsies import FullscreenWindow, Input

from game.comm import connect_socket, send_start, send_string, receive_string
from game.constants import *
from game import cfg

from game.view import view


def init():
    model = {
        # choices or grammar
        'response': ('choices', ['CHOICE_0', 'CHOICE_1']),
        'description': 'DESCRIPTION',
        'header': 'HEADER',
        'buffer': '',
        'last': '',
        'log': '',
        'candidates': [],
        'socket': None,
        'history': (-1, []),
        'view_template': '{buffer}|{choices}',
    }
    return model


def run():
    model = init()
    history = []
    with open('logs/term', 'w') as fh:
        print('started', file=fh)
        print('model', model, file=fh)
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
    response_type = m['response'][0]
    send = None
    if c == None:
        pass
    elif c in SYSTEM_CODES:
        send = SYSTEM_CODES[c]
    elif response_type == 'grammar':
        # special grammar buffer handling
        grammar = m['response'][1]
        new_buffer, send = update_buffer_grammar(grammar, m['buffer'], c)
        m['buffer'] = new_buffer
    elif response_type == 'choices':
        # regular buffer handling
        m, send = update_buffer_choices(m, c)
    if send != None:
        send_string(m['socket'], send)
    return m


def update_buffer_choices(model, c):
    m = model
    send = None
    choices = model['response'][1]
    if c == '<BACKSPACE>':
        m['buffer'] = m['buffer'][:-1]
    # if complete or uniquely autocompleted, send buffer as message to server
    elif c == '<SPACE>':
        m['candidates'] = [x for x in choices if x.lower().startswith(m['buffer'])]
        if len(m['candidates']) == 1:
            m['buffer'] = m['candidates'][0]
        if m['buffer'] in choices:
            word = m['buffer']
            m['last'] = word
            m['buffer'] = ''
            m['candidates'] = choices
            send = word
    elif any(x.lower().startswith(m['buffer'] + c.lower()) for x in choices):
        m['buffer'] = (m['buffer'] + c).lower()
        m['candidates'] = [x for x in choices if x.lower().startswith(m['buffer'])]
    return m, send


def update_buffer_grammar(grammar, buffer, character):
    """Almost identical to old Elm Typewriter. Except <DELETE>
    backspace to delete entire word.
    """
    pat = '(\w+ )'
    completed_words = [x.strip() for x in re.findall(pat, buffer)]
    choices = cfg.choices(grammar, completed_words)
    word_in_progress = buffer.split(' ')[-1]
    candidates = [x for x in choices if x.startswith(word_in_progress)]
    if word_in_progress:
        buffer_minus_word = buffer[:-len(word_in_progress)]
    else:
        buffer_minus_word = buffer
    ready_to_send = cfg.is_complete(grammar, completed_words)

    send = None

    # Set default value? Had issues here sometimes
    new_buffer = ''

    # autocomplete if there's only one word, and space is hit
    if character == '<SPACE>':
        if ready_to_send and word_in_progress == '':
            send = buffer_minus_word.strip()
            new_buffer = ''  
        elif len(candidates) == 1:
            new_buffer = buffer_minus_word + candidates[0] + ' '
    elif character == '<BACKSPACE>':
        if word_in_progress == '':
            new_buffer = buffer[:-2]
        else:
            new_buffer = buffer[:-1]
    elif character == '<DELETE>':
        if word_in_progress:
            new_buffer = buffer_minus_word
        else:
            new_buffer = ' '.join(completed_words[:-1])
    else:
        possible = word_in_progress + character
        for x in candidates:
            if x.lower().startswith(possible.lower()):
                new_buffer = buffer_minus_word + x[:len(word_in_progress) + 1]
                break
        else:
            # no match, no update
            new_buffer = buffer
    return new_buffer, send


def update_candidates(model):
    m = model
    if m['response'][0] == 'grammar':
        grammar = m['response'][1]
        pat = '(\w+ )'
        completed_words = [x.strip() for x in re.findall(pat, m['buffer'])]
        word_in_progress = m['buffer'].split(' ')[-1]
        choices = cfg.choices(grammar, completed_words)
        m['candidates'] = [x for x in choices if x.startswith(word_in_progress)]
    elif m['response'][0] == 'choices':
        choices = m['response'][1]
        m['candidates'] = [x for x in choices if x.lower().startswith(m['buffer'])]
    return m


if __name__ == '__main__':
    run()