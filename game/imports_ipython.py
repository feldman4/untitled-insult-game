import IPython
from IPython.display import display, Image
IPython.get_ipython().run_line_magic('load_ext', 'autoreload')
IPython.get_ipython().run_line_magic('autoreload', '2')
IPython.get_ipython().run_line_magic('matplotlib', 'inline')

from game import app, term
from game.constants import *