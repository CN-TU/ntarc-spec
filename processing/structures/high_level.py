import json
import six


class Flow(object):
    def __init__(self, d):
        if isinstance(d, six.string_types):
            d = json.load(open(d, 'r'))
        self.features = _get(d, 'features')
        self.goals = _get(d, 'goals')
        self.key = _get(d, 'key')
        self.tool = _get(d, 'tool')
        self.window = _get(d, 'window')


class Packet(object):
    def __init__(self, d):
        if isinstance(d, six.string_types):
            d = json.load(open(d, 'r'))
        self.features = _get(d, 'features')
        self.goals = _get(d, 'goals')


class FlowAggregation(object):
    def __init__(self, d):
        if isinstance(d, six.string_types):
            d = json.load(open(d, 'r'))
        self.features = _get(d, 'features')
        self.goals = _get(d, 'goals')
        self.key = _get(d, 'key')
        self.tool = _get(d, 'tool')
        self.window = _get(d, 'window')


class Method(object):
    def __init__(self, d):
        if isinstance(d, six.string_types):
            d = json.load(open(d, 'r'))
        self.name = _get(d, 'name')
        self.supervision = _get(d, 'supervision')
        self.type = _get(d, 'type')
        self.similarity_metric = _get(d, 'similarity_metric')


class Evaluation(object):
    _metrics = ['error_rate', 'classification_loss', 'error_rate_variation', 'error_distance', 'clustering_metrics',
                'time', 'space']
    _method_evaluation = ['internal', 'external', 'both']

    def __init__(self, d):
        if isinstance(d, six.string_types):
            d = json.load(open(d, 'r'))
        self.metrics = _get(d, 'metrics')
        if not self.metrics is None:
            for m in self.metrics:
                assert m in self._metrics, "Unknown metric %s!" % (m)

        self.method_evaluation = _get(d, 'method_evaluation')
        if not self.method_evaluation is None:
            assert self.method_evaluation in self._method_evaluation, "Unknown method of evaluation %s!" % \
                                                                      (self.method_evaluation)


class Dataset(object):
    _datasets_file = '../datasets.json'

    def __init__(self, d):
        self.key = d
        with open(self._datasets_file) as fd:
            try:
                parsed = json.load(fd)
            except:
                assert False, "Error parsing datasets file!"
            assert d in parsed, "Unknown dataset %s!" % (d)
        self._data = parsed[self.key]

    @property
    def availability(self):
        return self._data['availability']

    @property
    def type(self):
        return self._data['type']


def _get(d, key):
    try:
        return d[key]
    except KeyError:
        return None