import random
import sys
from itertools import cycle
import socket

from curtsies import FullscreenWindow, Input, FSArray
from curtsies.fmtfuncs import red, blue, bold, green, on_blue, yellow

from constants import PORT

"""
Want this process to listen to a socket AND keypresses.
"""

allowed = ['apple', 'appman', 'banana']


def add_header(a):
    msg = green(bold('Listening...'))


def add_to_second_line(a, msg):
    a[2, 0:len(msg)] = [red(msg)]


def run(sockets=False):
    header = 'Type your shit:'
    buffer = ''
    last = ''
    log = 'LOG'
    candidates = allowed
    
    if sockets:
        client = socket.socket()
        address=("localhost", PORT)
        client.connect(address)
        client.settimeout(0.1)

    with FullscreenWindow() as window, Input() as input_generator:
        while True:
            a = FSArray(window.height, window.width)
            first_row = red(header + last)
            second_row = blue(buffer)
            third_row = green(' '.join(candidates))
            fourth_row = red(log)

            a[0, :first_row.width] = [first_row]
            a[1, :second_row.width] = [second_row]
            a[2, :third_row.width] = [third_row]
            a[3, :fourth_row.width] = [fourth_row]
            window.render_to_terminal(a)

            # grab the next character
            c = input_generator.send(1)
            # buffer = str(type(/c))
            if c == None:
                continue
            if any(x.startswith(buffer + c) for x in allowed):
                buffer += c

            candidates = [x for x in allowed if x.startswith(buffer)]

            if c == '<SPACE>':
                if len(candidates) == 1:
                    buffer = candidates[0]
                if buffer in allowed:
                    last = buffer
                    buffer = ''
                    candidates = allowed

            if sockets:
                # read from socket
                incoming = client.recv(1024).decode()
                if incoming:
                    log += ' | ' + incoming


if __name__ == '__main__':
    run()
