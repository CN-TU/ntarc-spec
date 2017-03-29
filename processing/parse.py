import os
import six
import json
from structures.metadata import MetaPaper


def parse_file(fd):
    if isinstance(fd, six.string_types):
        if os.path.isfile(fd):
            fd = open(fd)
        else:
            raise FileNotFoundError('No such file ' + fd)
    d = json.load(fd)
    return parse(d)


def parse(d):
    return MetaPaper(d)

