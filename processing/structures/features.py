import json
import numbers
import six
import sys
import re
from . import PROJECT_PATH
import types
def copy_func(f, name=None):
    return types.FunctionType(f.__code__, f.__globals__, name or f.__name__,
        f.__defaults__, f.__closure__)


IANA_IE_LIST = PROJECT_PATH + '/data/iana_ies.csv'
OWN_IE_LIST = PROJECT_PATH + '/data/own_ies.csv'
SPECIFICATION_FILE = PROJECT_PATH + '/specification.txt'
CONVERSION_FILE = PROJECT_PATH + '/data/feature_aliases.json'
CONVERSION_D = None


def _generate_argument_checker(funcs):
    def check(x):
        ii = 0
        for ff in funcs:
            try:
                res = ff(x[ii:])
            except:
                return False
            if res:
                if res == 'star':
                    continue
                ii += res
        if ii < len(x):
            return False
        else:
            return True
    return check


def _generate_type_comparison(n):
    def check(x):
        return x.type == n
    return check


def _generate_plus_f(n):
    def plus_f(x, new_i=0):
        while new_i < len(x) and _generate_type_comparison(n)(x[new_i]):
            new_i += 1
        return new_i
    return plus_f


def _generate_times_f(n):
    def times_f(x, new_i=0):
        while new_i < len(x) and _generate_type_comparison(n)(x[new_i]):
            new_i += 1
        return new_i if new_i > 0 else 'star'
    return times_f


def _generate_one_f(n):
    def one_f(x):
        return _generate_type_comparison(n)(x[0])
    return one_f


class Operation(object):
    def __init__(self, line):
        line = line.split(' #')[0]
        self.type = line.split('>')[0].split('<')[-1]
        self.name = line.split('":')[0].split('"')[-1]
        possibilities = line.split('->')[-1].split('|')
        self.argument_possibilities = []
        for arg in possibilities:
            if '"' not in arg:  # skip lines that don't have operations
                continue
            new_arg = re.sub(r'>([+*]*)', r'>\1"', arg.replace('<', '"<'))
            d = json.loads(new_arg)
            args = d[self.name]
            funcs = []
            for aa in args:
                n = FeatureType(aa.split('>')[0].split('<')[-1])
                if aa[-1] == '+':  # allow multiple arguments, require at least 1
                    f = _generate_plus_f(n)
                elif aa[-1] == '*':  # allow multiple arguments (or none)
                    f = _generate_times_f(n)
                else:
                    f = _generate_one_f(n)
                funcs.append(f)
            final_f = _generate_argument_checker(funcs)
            self.argument_possibilities.append(final_f)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name



def _get_iana_ies(filename):
    out = set()
    with open(filename, 'rb') as fd:
        fd.readline()  # skip headers
        text = fd.read().split(b'\r\n')
        for line in text:
            line = line.decode()
            if len(line) > 0:
                out.add(line.split(',')[1])
    return out


def _get_own_ies(filename):
    out = set()
    with open(filename) as fd:
        for line in fd:
            out.add(line.split(',')[0])
    return out


def _get_aliases(filename):
    with open(filename) as fd:
        d = json.load(fd)
        out = set(list(d.keys()))
    return out


def _get_arguments_dict_from_specification(filename, keyword):
    out = {}
    l = len(keyword)
    with open(filename) as fd:
        for line in fd:
            if line[1:(l + 1)] == keyword:
                op = Operation(line)
                out[op.name] = op
    return out


class FeatureType(object):
    try:
        _specification = open(SPECIFICATION_FILE).readlines()
    except:
        _specification = None

    def __init__(self, name):
        self.name = name
        self.parents = self._get_parents(name)

    @staticmethod
    def _get_parents(name):
        if FeatureType._specification is None:
            raise ValueError('Please define PROJECT_PATH in config file!')

        out = set()
        for line in FeatureType._specification:
            line = line.split('#')[0] if line[0] != '#' else ''  # remove comments
            if '"' in line or '<' + name + '>' not in line.split('->')[-1]:  # skip if name isn't there
                continue
            line = line.split('->')
            out.add(line[0].split('>')[0].split('<')[-1])

        new_out = set()
        for t in out:
            new_out.add(t)
            new_out.update(FeatureType._get_parents(t))

        return new_out

    def __eq__(self, other):
        return self.name == other.name or other.name in self.parents or self.name in other.parents


def _convert_feature(feature):
    global CONVERSION_D
    if CONVERSION_D is None:
        CONVERSION_D = json.load(open(CONVERSION_FILE, 'r'))
    if isinstance(feature, six.string_types) and feature in CONVERSION_D:
        return _convert_feature(CONVERSION_D[feature])
    else:
        return feature


class Features(object):
    def __init__(self, d):
        self.features = [Feature(f) for f in d['features']]

    def iterate_features(self):
        return Features._iterate_base_features(self.features)

    def get_base_feature_names(self):
        return set([f.feature for f in self.iterate_features()])

    def get_operation_names(self):
        ops = set([f.key for f in Features._iterate_operations(self.features)])
        return ops

    @staticmethod
    def _iterate_operations(features):
        for f in features:
            for ff in Feature._iterate_operations(f):
                yield ff

    @staticmethod
    def _iterate_base_features(features):
        for f in features:
            for ff in Feature._iterate_base_features(f):
                yield ff


class Feature(object):
    _iana_ies = _get_iana_ies(IANA_IE_LIST)
    _own_features = _get_own_ies(OWN_IE_LIST)
    _aliases = _get_aliases(CONVERSION_FILE)
    _base_features = _iana_ies | _own_features | _aliases

    _operations_dict = _get_arguments_dict_from_specification(SPECIFICATION_FILE, 'value')
    _logic_dict = _get_arguments_dict_from_specification(SPECIFICATION_FILE, 'logic')
    _values_dict = _get_arguments_dict_from_specification(SPECIFICATION_FILE, 'values')
    _selection_dict = _get_arguments_dict_from_specification(SPECIFICATION_FILE, 'selection')
    _all_operations_dict = {"value": _operations_dict, "logic": _logic_dict, "values": _values_dict,
                            "selection": _selection_dict}


    _operations = set(_operations_dict.keys()) | set(["basedon"])
    _logic = set(_logic_dict.keys())
    _values = set(_values_dict.keys())
    _selection = set(_selection_dict.keys())
    operations = _operations | _logic | _values | _selection

    def __init__(self, feature):
        feature = _convert_feature(feature)
        self.feature = feature
        if type(feature) is dict:
            keys = list(feature)
            assert len(keys) == 1, 'There should only be one key! Keys are: ' + str(keys)
            key = keys[0]
            self.key = key
            if key in self._operations:
                self.type = FeatureType('value')
            elif key in self._logic:
                self.type = FeatureType('logic')
            elif key in self._values:
                self.type = FeatureType('values')
            elif key in self._selection:
                self.type = FeatureType('selection')
            else:
                raise ValueError('No such operation defined: ' + key)
        elif isinstance(feature, six.string_types):
            self.type = FeatureType('base-feature')
            self.key = None
            assert feature in self._base_features or feature[:2] == '__', 'Unknown base feature ' + feature
        elif isinstance(feature, bool):
            self.type = FeatureType('logic')
            self.key = None
        elif isinstance(feature, numbers.Number):
            self.type = FeatureType('value')
            self.key = None
        else:
            raise ValueError('Invalid feature ' + feature)

        if self.key is not None:
            assert type(feature[self.key]) is list, 'Arguments need to be in a list! Fail in ' + feature
            self.arguments = [Feature(f) for f in feature[self.key]]
        else:
            self.arguments = None

        # test arguments
        if self.arguments is not None and 'basedon' not in self.feature:
            op = self._all_operations_dict[self.type.name][self.key]
            res = any([test(self.arguments) for test in op.argument_possibilities])
            if not res:
                print('Error!', json.dumps(self.feature), ', Received arguments to "' + self.key + '":',
                      str([arg.type.name for arg in self.arguments]))

    @staticmethod
    def _iterate_base_features(feature):
        if feature.type.name == 'base-feature':
            yield feature
        elif feature.arguments is not None:
            for arg in feature.arguments:
                for feat in Feature._iterate_base_features(arg):
                    yield feat

    @staticmethod
    def _iterate_operations(feature):
        if feature.arguments is not None:
            yield feature
            for f in feature.arguments:
                for k in Feature._iterate_operations(f):
                    yield k
