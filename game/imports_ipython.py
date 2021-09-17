import re
from glob import glob
import pandas as pd
import numpy as np
import os

import IPython
from IPython.display import display, Image

IPython.get_ipython().run_line_magic('matplotlib', 'inline')

# get rid of annoying warning
import contextlib
with contextlib.redirect_stdout(open(os.devnull, 'w')):
    IPython.get_ipython().run_line_magic('load_ext', 'autoreload')
    IPython.get_ipython().run_line_magic('autoreload', '2')
del contextlib

from game import app, term, server, cfg, utils
from game.constants import *

import game
HOME = os.path.dirname(os.path.dirname(game.__file__))
del game

