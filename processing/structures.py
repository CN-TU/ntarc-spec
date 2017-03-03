import os
import six
import simplejson
import requests


CACHE_DIR = '/home/dferreira/projects/phd-df/processing_pcaps/feature_vectors/processing/.cache'


class Reference(object):
    def __init__(self, d):
        if isinstance(d, six.string_types):
            d = simplejson.load(open(d, 'r'))
        ref = d['reference']
        self._author_full = ref['author']
        self.author = ref['author'].replace('et al.', '').strip()
        self.title = ref['title']
        self.year = ref['year']
        self._data = None

    def __repr__(self):
        return self._author_full + ' ' + str(self.year)

    @property
    def _cache_filename(self):
        return CACHE_DIR + os.sep + self.author + str(self.year) + self.title[:5]

    def _check_cache(self):
        return os.path.isfile(self._cache_filename)

    def _write_cache(self, data):
        with open(self._cache_filename, 'w') as fd:
            simplejson.dump(data, fd)

    def _load_cache(self):
        with open(self._cache_filename, 'r') as fd:
            self._data = simplejson.load(fd)

    def _query(self):
        if not self._check_cache():
            url_base = 'https://api.projectoxford.ai/academic/v1.0/evaluate'
            url_base = 'https://westus.api.cognitive.microsoft.com/academic/v1.0/evaluate'
            title = "Ti='" + ''.join(e if e.isalnum() else ' ' for e in self.title.lower()).replace('  ', ' ') + "'"
            year = "Y=[" + str(self.year - 1) + ',' + str(self.year + 1) + ']'
            expr = "And(" + title + ', ' + year + ')'
            attrs = 'Id,Ti,AA.AuN,ECC,E'
            api_key = '55ebf3d7a5d04e3f91810a8cf9796d2a'

            url = url_base
            url += '?expr=' + expr
            url += '&attributes=' + attrs
            r = requests.get(url, headers={'Ocp-Apim-Subscription-Key': api_key})
            data = r.json()
            if 'entities' not in data or len(data['entities']) != 1:
                print(self.author, self.title)
                print(expr)
                print()
            self._data = data['entities'][0]
            self._write_cache(self._data)
        else:
            self._load_cache()

    @property
    def data(self):
        if self._data is None:
            self._query()
        return self._data

    @property
    def citations(self):
        return self.data['ECC']


CONVERSION_FILE = '/home/dferreira/projects/phd-df/processing_pcaps/feature_vectors/dict.json'
CONVERSION_D = None


def _convert_feature(feature):
    global CONVERSION_D
    if CONVERSION_D is None:
        CONVERSION_D = simplejson.load(open(CONVERSION_FILE, 'r'))
    if isinstance(feature, six.string_types) and feature in CONVERSION_D:
        return _convert_feature(CONVERSION_D[feature])
    else:
        return feature


class Feature(object):
    _operations = {'features', 'mean', 'stdev', 'variance', 'minimum', 'maximum', 'argmin', 'argmax',
                  'count', 'distinct', 'apply', 'map', 'add', 'subtract', 'multiply', 'divide',
                  'entropy', 'get', 'get_previous', 'select'}
    logic = {'geq', 'leq', 'less', 'greater', 'equal', 'and', 'or'}
    operations = _operations | logic
    def __init__(self, feature):
        self.feature = feature

    @staticmethod
    def _iterate_base_features(feature):
        if isinstance(feature, six.string_types):
            feature = _convert_feature(feature)

        # note that this check is after `feature` has been converted (it is needed!)
        if isinstance(feature, six.string_types):
            yield feature
        if isinstance(feature, dict):
            keys = list(feature.keys())
            if len(keys) != 1:
                raise KeyError
            if keys[0] not in Feature.operations:
                raise KeyError('No such operation ' + keys[0])
            # return set().union(_get_base_features(f) for f in feature[keys[0]])
            for f in feature[keys[0]]:
                if isinstance(f, dict):
                    for ft in Feature._iterate_base_features(f):
                        yield ft
                elif isinstance(_convert_feature(f), dict):
                    for ft in Feature._iterate_base_features(_convert_feature(f)):
                        yield ft
                else:
                    yield Feature._iterate_base_features(f)

    @staticmethod
    def _iterate_operations(feature):
        if isinstance(feature, dict):
            keys = list(feature.keys())
            if len(keys) != 1:
                raise KeyError
            if keys[0] not in Feature.operations:
                raise KeyError('No such operation ' + keys[0])
            else:
                yield keys[0]
                for f in feature[keys[0]]:
                    for ft in Feature._iterate_operations(f):
                        yield ft

    def iterate_features(self):
        return Feature._iterate_base_features(self.feature)

    def get_features(self):
        return set(self.iterate_features())

    def get_operations(self):
        ops = set(Feature._iterate_operations(self.feature))
        return ops


class Flow(object):
    def __init__(self, d):
        if isinstance(d, six.string_types):
            d = simplejson.load(open(d, 'r'))
        self.features = _get(d, 'features')
        self.goals = _get(d, 'goals')
        self.key = _get(d, 'key')
        self.tool = _get(d, 'tool')
        self.window = _get(d, 'window')


class Packet(object):
    def __init__(self, d):
        if isinstance(d, six.string_types):
            d = simplejson.load(open(d, 'r'))
        self.features = _get(d, 'features')
        self.goals = _get(d, 'goals')
        self.key = _get(d, 'key')


class FlowAggregation(object):
    def __init__(self, d):
        if isinstance(d, six.string_types):
            d = simplejson.load(open(d, 'r'))
        self.features = _get(d, 'features')
        self.goals = _get(d, 'goals')
        self.key = _get(d, 'key')
        self.tool = _get(d, 'tool')
        self.window = _get(d, 'window')


class Method(object):
    def __init__(self, d):
        if isinstance(d, six.string_types):
            d = simplejson.load(open(d, 'r'))
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
            d = simplejson.load(open(d, 'r'))
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
            parsed = simplejson.load(fd)
            assert d in parsed, "Unknown dataset %s!" % (d)



def _get(d, key):
    try:
        return d[key]
    except KeyError:
        return None


if __name__ == '__main__':
    filename = '/home/dferreira/projects/phd-df/processing_pcaps/feature_vectors/papers/tegeler2012.json'
    ref = Reference(filename)
    print(ref.citations)
