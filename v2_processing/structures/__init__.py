import os
from .tool import Tool


PROJECT_PATH = os.path.join(os.sep.join(__file__.split('/')[:-1]), '..', '..')


def optional(d, key):
    try:
        return d[key]
    except KeyError:
        return None


from .blocks import *
from .high_level import FullPaper
