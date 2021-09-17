import fire

from game.utils import update_vocab, update_vocab_and_vectors

def term():
    """Run the curtsies front end.
    """
    from game import term
    term.run()


def server():
    """Run the backend.
    """
    from game import server
    server.run()


if __name__ == '__main__':
    fire.Fire()
