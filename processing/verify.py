from __future__ import print_function
import sys
import json
from structures import *


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

        ref = Reference(loaded)

        flow_count = len([Flow(f) for f in _get_or_empty(loaded, 'flows')])
        packet_count = len([Packet(f) for f in _get_or_empty(loaded, 'packets')])
        flow_agg_count = len([FlowAggregation(f) for f in _get_or_empty(loaded, 'flow_aggregations')])
        methods_count = len([Method(f) for f in _get_or_empty(loaded, 'methods')])
        evaluations_count = len([Evaluation(f) for f in _get_or_empty(loaded, 'evaluations')])
        datasets_count = len([Dataset(f) for f in _get_or_empty(loaded, 'datasets')])


    print('Reference:', ref)
    print('Nr of flows:', flow_count)
    print('Nr of packets:', packet_count)
    print('Nr of flow aggregations:', flow_agg_count)
    print('Nr of methods:', methods_count)
    print('Nr of evaluations:', evaluations_count)
    print('Nr of datasets:', datasets_count)
