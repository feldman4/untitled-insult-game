import fire
import sys

def term():
    from game import term
    term.run()

def server():
    from game import server
    server.run()

if __name__ == '__main__':
    fire.Fire()
