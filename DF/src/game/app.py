import fire
import sys


def term(sockets=False):
    from game import term
    term.run(sockets=sockets)


def sockets():
    from game import sockets


if __name__ == '__main__':
    fire.Fire()
