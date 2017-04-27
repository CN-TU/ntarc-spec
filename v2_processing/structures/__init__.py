try:
    from conf import PROJECT_PATH, API_KEY, MAPS_API_KEY, CACHE_DIR
except ImportError:
    PROJECT_PATH = ''
    API_KEY = ''
    MAPS_API_KEY = ''
from .tool import Tool


def optional(d, key):
    try:
        return d[key]
    except KeyError:
        return None

from .blocks import *
from .high_level import FullPaper