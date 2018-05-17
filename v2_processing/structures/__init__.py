from subprocess import check_output
from .tool import Tool


PROJECT_PATH = check_output(['git', 'rev-parse', '--top-level'])


def optional(d, key):
    try:
        return d[key]
    except KeyError:
        return None

from .blocks import *
from .high_level import FullPaper