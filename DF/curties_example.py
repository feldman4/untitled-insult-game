import random
import sys

from curtsies import FullscreenWindow, Input, FSArray
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow

print(yellow('this prints normally, not to the alternate screen'))

with FullscreenWindow() as window:
    a = FSArray(window.height, window.width)
    msg = red(on_blue(bold('Press escape to exit, space to clear.')))
    a[0:1, 0:msg.width] = [msg]
    window.render_to_terminal(a)
    with Input() as input_generator:
        for c in input_generator:
            if c == '<ESC>':
                break
            elif c == '<SPACE>':
                a = FSArray(window.height, window.width)
            else:
                s = repr(c)
                row = random.choice(range(window.height))
                column = random.choice(range(window.width-len(s)))
                color = random.choice([red, green, on_blue, yellow])
                a[row, column:column+len(s)] = [color(s)]
            window.render_to_terminal(a)
