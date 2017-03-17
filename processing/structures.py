import os
import six
import simplejson
import requests
import time
from conf import PROJECT_PATH, API_KEY


CACHE_DIR = PROJECT_PATH + '/processing/.cache'


class BaseEntity(object):
    url_base = 'https://westus.api.cognitive.microsoft.com/academic/v1.0/evaluate'
    api_key = API_KEY
    attrs = None

    def __init__(self, id):
        self._id = id
        self._data = None

    def _query_id_attrs(self, id, attrs):
        if not self._check_cache():
            expr = 'Id=' + str(id)

            url = self.url_base
            url += '?expr=' + expr
            url += '&attributes=' + attrs

            r = requests.get(url, headers={'Ocp-Apim-Subscription-Key': self.api_key})
            data = r.json()
            self._data = data['entities'][0]
            self._write_cache(self._data)
            time.sleep(1)
        else:
            self._load_cache()

    @property
    def id(self):
        return self.data['Id']

    @property
    def data(self):
        if self._data is None:
            self._query_id_attrs(self._id, self.attrs)
        return self._data

    def _check_cache(self):
        return os.path.isfile(self._cache_id_filename)

    @property
    def _cache_id_filename(self):
        raise NotImplementedError

    def _write_cache(self, data):
        with open(self._cache_id_filename, 'w') as fd:
            simplejson.dump(data, fd)

    def _load_cache(self):
        with open(self._cache_id_filename, 'r') as fd:
            self._data = simplejson.load(fd)

    def _query_id(self, id):
        self._query_id_attrs(id, self.attrs)


class Author(BaseEntity):
    attrs = 'Id,AuN,DAuN,CC,ECC,E,SSD'

    @property
    def _cache_id_filename(self):
        return CACHE_DIR + os.sep + 'author_id' + os.sep + str(self._id)


class Affiliation(BaseEntity):
    attrs = 'Id,AfN,DAfN,CC,ECC,SSD'

    @property
    def _cache_id_filename(self):
        return CACHE_DIR + os.sep + 'affiliation_id' + os.sep + str(self._id)


class Journal(BaseEntity):
    attrs = 'Id,DJN,JN,CC,ECC,SSD'

    @property
    def _cache_id_filename(self):
        return CACHE_DIR + os.sep + 'journal_id' + os.sep + str(self._id)


class ConferenceSeries(BaseEntity):
    attrs = 'Id,CN,DCN,CC,ECC,F.FId,F.FN,SSD'

    @property
    def _cache_id_filename(self):
        return CACHE_DIR + os.sep + 'conferenceseries_id' + os.sep + str(self._id)


class ConferenceInstance(BaseEntity):
    attrs = 'Id,CIN,DCN,CIL,CISD,CIED,CIARD,CISDD,CIFVD,CINDD,CD.T,CD.D,PCS.CN,PCS.CId,CC,ECC,SSD'

    @property
    def _cache_id_filename(self):
        return CACHE_DIR + os.sep + 'conferenceinstance_id' + os.sep + str(self._id)


class FieldOfStudy(BaseEntity):
    attrs = 'Id,FN,DFN,CC,ECC,FL,FP.FN,FP.FId,SSD'

    @property
    def _cache_id_filename(self):
        return CACHE_DIR + os.sep + 'fieldofstudy_id' + os.sep + str(self._id)


class Reference(BaseEntity):
    attrs = 'Id,Ti,L,Y,D,CC,ECC,AA.AuN,AA.AuId,AA.AfN,AA.AfId,F.FN,F.FId,J.JN,J.JId,C.CN,C.CId,RId,W,E'

    def __init__(self, d):
        if isinstance(d, six.integer_types):
            self._id = d
            self._author = None
            self._title = None
            self._year = None
            self._data = None
            self._query_id(d)
        else:
            if isinstance(d, six.string_types):
                d = simplejson.load(open(d, 'r'))
            ref = d['reference']
            self._author_full = ref['author']
            self._author = ref['author'].replace('et al.', '').strip()
            self._title = ref['title']
            self._year = ref['year']
            self._id = ref['id'] if 'id' in ref else None
            self._data = None

    def __repr__(self):
        return self._author_full + ' ' + str(self.year)

    @property
    def year(self):
        if self._year is not None:
            return self._year
        else:
            return self.data['Y']

    @property
    def title(self):
        if self._title is not None:
            return self._title
        else:
            try:
                return self.data['E']['DN']
            except:
                return self.data['Ti']

    @property
    def author(self):
        if self._author is not None:
            return self._author
        else:
            return self.data['AA'][0]['AuN']

    @property
    def _cache_filename(self):
        return CACHE_DIR + os.sep + 'paper_map' + os.sep + self.author + str(self.year) + self.title[:5]

    @property
    def _cache_id_filename(self):
        return self.get_cache_filename(self.id)

    def get_cache_filename(self, id):
        return CACHE_DIR + os.sep + 'paper_id' + os.sep + str(id)

    def _check_cache(self):
        if self._author is None:
            return os.path.isfile(self.get_cache_filename(self._id))
        else:
            return os.path.isfile(self._cache_filename)

    def _write_cache(self, data):
        with open(self._cache_filename, 'w') as fd:
            fd.write(str(self.id))
        with open(self._cache_id_filename, 'w') as fd:
            simplejson.dump(data, fd)

    def _load_cache(self):
        try:
            with open(self._cache_filename, 'r') as fd:
                id = int(fd.read())
        except:
            id = self._id
        with open(self.get_cache_filename(id), 'r') as fd:
            self._data = simplejson.load(fd)

    def _query_id(self, id):
        self._query_id_attrs(id, self.attrs)

    def _query(self):
        if not self._check_cache():
            title = "Ti='" + ''.join(e if e.isalnum() else ' ' for e in self.title.lower()).replace('  ', ' ') + "'"
            year = "Y=[" + str(self.year - 1) + ',' + str(self.year + 1) + ']'
            expr = "And(" + title + ', ' + year + ')'

            url = self.url_base
            url += '?expr=' + expr
            url += '&attributes=' + self.attrs
            r = requests.get(url, headers={'Ocp-Apim-Subscription-Key': self.api_key})
            data = r.json()
            if 'entities' not in data or len(data['entities']) != 1:
                print(self.author, self.title)
                print(expr)
                print()
            try:
                self._data = data['entities'][0]
            except IndexError:
                if self._id is not None:
                    self._query_id(self._id)
                else:
                    raise IndexError
            self._write_cache(self._data)
            time.sleep(1)
        else:
            self._load_cache()

    @property
    def data(self):
        if self._data is None:
            if self._id is None:
                self._query()
            else:
                self._query_id_attrs(self._id, self.attrs)
        return self._data

    @property
    def citations(self):
        return self.data['ECC']

    @property
    def bibliography(self):
        return [Reference(id) for id in self.data['RId']] if 'RId' in self.data else []

    @property
    def affiliations(self):
        return [Affiliation(auth['AfId']) for auth in self.data['AA'] if 'AfId' in auth]


CONVERSION_FILE = PROJECT_PATH + '/dict.json'
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
                  'entropy', 'get', 'get_previous', 'select', 'log', 'exp', 'slice', 'ifelse', 'basedon', 'quantile',
                   'median', 'left_shift', 'right_shift', 'mode'}
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
            try:
                parsed = simplejson.load(fd)
            except:
                assert False, "Error parsing datasets file!"
            assert d in parsed, "Unknown dataset %s!" % (d)



def _get(d, key):
    try:
        return d[key]
    except KeyError:
        return None
