import fire
import sys

def term():
    from game import term
    term.run()

def sockets():
    from game import sockets

if __name__ == '__main__':
    fire.Fire()