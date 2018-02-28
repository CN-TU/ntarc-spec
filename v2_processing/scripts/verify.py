from __future__ import print_function
import sys
import json
from v2_processing.structures import FullPaper


# Needs environment variable PYTHONPATH=project_directory


def _get_or_empty(d, key):
    try:
        return d[key] if d[key] is not None else []
    except KeyError:
        return []


if __name__ == '__main__':
    fname = sys.argv[1]

    with open(fname) as fd:
        # test json loading
        loaded = json.load(fd)

        paper = FullPaper(loaded)

    # print('Reference:', ref)
    # print('Nr of flows:', flow_count)
    # print('Nr of packets:', packet_count)
    # print('Nr of flow aggregations:', flow_agg_count)
    # print('Nr of methods:', methods_count)
    # print('Nr of evaluations:', evaluations_count)
    # print('Nr of datasets:', datasets_count)
