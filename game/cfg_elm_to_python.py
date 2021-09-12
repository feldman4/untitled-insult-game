"""David's 2016 CFG Elm code, 2021 back-translation to python (!?)
"""

def extend(grammar, sentence):
    """Find all extensions of a sentence reached by
    applying one production."""
    arr = []
    for i, x in enumerate(sentence):
        chains = getChains(grammar, x)
        arr += [sentence[:i] + c + sentence[i+1:] for c in chains]
    return arr

def extendFirst(grammar, sentence):
    """Find extensions of a sentence reached by applying just the first
    production that matches from the left.
    """
    for i, x in enumerate(sentence):
        if x[0] != 'Terminal':
            chains = getChains(grammar, x)
            return [sentence[:i] + c + sentence[i+1:] for c in chains]
    return [sentence + [Terminal('')]]

def isMismatch(grammar, soFar, sentence):
    """Checks if list of contiguous terminals at the start of candidate sentence
    matches the sentence soFar. Used to remove wrong branches when expanding
    a grammar to match the sentence soFar."""
    prefix = terminalPrefix(sentence)
    return not all(a == b for a,b in zip(soFar, prefix))

def isValidExtension(grammar, soFar, sentence):
    """Check if sentence matches terminals in so_far, and the next symbol
    is a terminal.
    """
    for a,b in zip(soFar, sentence):
        if a!=b:
            return False
    if len(soFar) >= len(sentence):
        return True
    # check the last terminal
    return soFar[len(sentence)][0] == 'Terminal'


def terminalPrefix(sentence):
    arr = []
    for x in sentence:
        if x[0] == 'Terminal':
            arr += [x]
        else:
            return arr
    return arr

def getChains(grammar, symbol):
    return [rhs for lhs, rhs in grammar if lhs == symbol]
            

def getTerminals(grammar):
    arr = []
    for _, xs in grammar:
        arr += [b for a,b in xs if a == 'Terminal']
    return arr