import re
import json
from ... import PROJECT_PATH


IANA_IE_LIST = PROJECT_PATH + '/iana_ies.csv'
OWN_IE_LIST = PROJECT_PATH + '/own_ies.csv'
SPECIFICATION_FILE = PROJECT_PATH + '/specification.txt'
CONVERSION_FILE = PROJECT_PATH + '/feature_aliases.json'


specification = open(SPECIFICATION_FILE).readlines()


class FeatureError(Exception):
    def __init__(self, input_argument, attempt, message):
        self.input_argument = input_argument
        self.attempt = attempt
        self.message = message


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
    return d


def get_rules(target):
    out = []
    match_line = re.compile('^<'+target+'> -> ')
    for line in specification:
        if match_line.match(line):  # check if line has rule for target
            options = [x.strip() for x in line.split('->')[1].split('#')[0].split('|')]
            out.extend(options)
    return out


def get_operations(rules):
    out = {}
    op_regex = re.compile('^\{\s*"\w+":\s*\[.*\]\s*\}$')
    for rule in rules:
        if op_regex.match(rule):  # check if rule is an operation
            key = rule.split('"')[1]
            arguments = [x for x in rule.split('[')[-1].split(']')[0].split(',')]
            if key not in out:
                out[key] = []
            out[key].append(arguments)
    return out


def get_non_term_symbols(rules):
    out = []
    symb_regex = re.compile('^\s*\<[\w0-9-]+\>\s*$')
    for rule in rules:
        if symb_regex.match(rule):
            out.append(rule)
    return out


def get_term_symbols(rules):
    out = []
    symb_regex = re.compile('^\s*"\w+"\s*$')
    non_quoted_regex = re.compile('^\w*$')
    for rule in rules:
        if symb_regex.match(rule):
            out.append(rule.strip('"'))
        elif non_quoted_regex.match(rule):
            out.append(json.loads(rule))
    return out


def match_arguments(op_args, input_args, level):
    if len(op_args) != len(input_args) and ('+' not in str(op_args) and '*' not in str(op_args)):
        raise FeatureError(input_args, op_args, 'Wrong size!')  # check for basic input structure
    out = []
    idx = 0
    for arg in op_args:
        arg = arg.strip()
        if arg[-1] in ['+', '*']:
            parsed_args = []
            while idx < len(input_args):
                try:
                    parsed_args.append(parse_as(input_args[idx], arg[:-1], level))
                    idx += 1
                except FeatureError:
                    break
            if arg[-1] == '+' and len(parsed_args) <= 0:
                raise FeatureError(input_args[idx:], arg, 'Need to consume at least one argument (consumed 0)!')
            out.extend(parsed_args)
        else:
            out.append(parse_as(input_args[idx], arg, level))
            idx += 1
    if len(out) != len(input_args):
        raise FeatureError(input_args, op_args, 'Not all arguments were consumed!')

    return out


def parse_as(argument, name, level):
    return possible_types[name.strip('<>')](argument, level)


class Base(object):
    name = None
    rules = None
    ops = None
    non_term = None
    term = None
    leaf = False
    aliases = _get_aliases(CONVERSION_FILE)

    def __init__(self, d, level):
        self.level = level
        if self.name in ['down', 'down2']:
            self.level -= 1
        if self.level < 0:
            raise FeatureError(d, self.name, "Already at bottom level, can't go further down.")

        if type(d) == str and d in self.aliases:
            d = self.aliases[d]

        self.key = None
        self.arguments = None
        self.possible_parses = []
        self.basefeat = None
        self.errors = []

        self.parse(d)

    def parse(self, d):
        try:
            self.parse_as_self(d)
        except FeatureError as e:
            self.errors.append(e)
            try:
                self.parse_non_terminal(d)
            except FeatureError as e:
                self.errors.append(e)
        if len(self.possible_parses) == 0:
            raise FeatureError(d, self.name, self.errors)

    def parse_as_self(self, d):
        # op
        if type(d) == dict:
            # check if op exists
            assert len(d.keys()) == 1, 'Only one operation at a time is allowed!'
            self.key = list(d.keys())[0]
            if self.key not in self.ops:
                raise FeatureError(d, self.name, 'No such operation!')
            self.arguments = d[self.key]

            # validate arguments
            for op in self.ops[self.key]:
                try:
                    args = match_arguments(op, self.arguments, self.level)
                    self.possible_parses.append(args)
                except FeatureError as e:
                    self.errors.append(e)
                    continue
            if len(self.possible_parses) == 0:
                raise FeatureError(d, self.name, "Can't parse directly!")

        elif type(d) in [str, int, float, bool]:
            # terminal symbol
            for symbol in self.term:
                if symbol == d:
                    self.possible_parses = [symbol]
            if len(self.possible_parses) == 0:
                raise FeatureError(d, self.name, 'Doesn\'t match any terminal symbol.')
        else:
            raise FeatureError(d, self.name, "Can't parse (wrong type)!")


    def parse_non_terminal(self, d):
        # non-terminal symbol
        for symbol in self.non_term:
            try:
                arg = parse_as(d, symbol, self.level)
                self.possible_parses.append(arg)
            except FeatureError as e:
                self.errors.append(e)
                continue
        if len(self.possible_parses) == 0:
            raise FeatureError(d, self.name, "Doesn't match any non-terminal symbol.")

    def iterate_operations(self):
        if self.key is not None:
            yield self.key
        if not self.leaf:
            if type(self.possible_parses[0]) == list:
                for arg in self.possible_parses[0]:
                    for op in arg.iterate_operations():
                        yield op
            else:
                for op in self.possible_parses[0].iterate_operations():
                    yield op

    def iterate_base_features(self):
        if self.basefeat is not None:
            yield self.basefeat
        elif not self.leaf:
            if type(self.possible_parses[0]) == list:
                for arg in self.possible_parses[0]:
                    for feat in arg.iterate_base_features():
                        yield feat
            else:
                for feat in self.possible_parses[0].iterate_base_features():
                    yield feat


def get_type(inp_name):
    rules = get_rules(inp_name)
    ops = get_operations(rules)
    non_term = get_non_term_symbols(rules)
    term = get_term_symbols(rules)

    new_class = type(inp_name.capitalize(),
                     (Base,),
                     {
                         'name': inp_name,
                         'rules': rules,
                         'ops': ops,
                         'non_term': non_term,
                         'term': term
                     })

    return new_class


class BaseFeature(Base):
    name = 'base-feature'
    iana_ies = _get_iana_ies(IANA_IE_LIST)
    own_ies = _get_own_ies(OWN_IE_LIST)
    # aliases = _get_aliases(CONVERSION_FILE)
    rare_feature = re.compile('^__[a-z0-9]+([A-Z][a-z0-9]*)*$')
    leaf = True

    def parse(self, d):
        if type(d) != str:
            raise FeatureError(d, self.name, 'Base features need to be strings!')
        if not self.rare_feature.match(d) and \
                        d not in self.own_ies and \
                        d not in self.iana_ies:
            raise FeatureError(d, self.name, 'Base feature doesn\'t exist or has invalid name!')
        self.basefeat = d


class Number(Base):
    name = 'free-number'
    leaf = True

    def parse(self, d):
        if type(d) not in [int, float]:
            raise FeatureError(d, self.name, 'Not a number!')


possible_types = {k: get_type(k) for k in ['value', 'values', 'selection', 'down', 'logic', 'logic-down', 'down2']}
possible_types['base-feature'] = BaseFeature
possible_types['free-integer'] = Number
possible_types['free-float'] = Number


class Features(object):
    def __init__(self, d, level):
        self.features = [possible_types['value'](f, level) for f in d]

    def iterate_features(self):
        return self.iterate_base_features()

    def get_base_feature_names(self):
        return set(self.iterate_features())

    def get_operation_names(self):
        ops = set(self.iterate_operations())
        return ops

    def iterate_operations(self):
        for f in self.features:
            for ff in f.iterate_operations():
                yield ff

    def iterate_base_features(self):
        for f in self.features:
            for ff in f.iterate_base_features():
                yield ff


if __name__ == '__main__':
    # some features that should work
    packet_features = [
        "octetTotalCount"
    ]
    flow_features = [
        "_flowDurationSeconds",
        # total octetTotalCount
        "octetTotalCount",
        # mean of octetTotalCount in packets
        {"mean": ["octetTotalCount"]},
        # mean of octetTotalCount in packets that have less than 1000 octetTotalCount
        {"mean": [{"map": ["octetTotalCount",
                           {"select": [{"less": ["octetTotalCount", 1000]}]}]}]},
        {
            "count": [
              {
                "select": [
                  {
                    "equal": [
                      "ipClassOfService",
                      {
                        "mode": [
                          "ipClassOfService"
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
    ]
    flowagg_features = [
        "_flowDurationSeconds",
        # total octetTotalCount
        "octetTotalCount",
        # mean of octetTotalCount in flows
        {"mean": ["octetTotalCount"]},
        # mean of octetTotalCount in flows with less than 1000 octetTotalCount
        {"mean": [{"map": ["octetTotalCount",
                           {"select": [{"less": ["octetTotalCount", 1000]}]}]}]},
        # mean (over flows) of mean (over packets) of octetTotalCount (using map twice)
        {"mean": [{"map": [
            {"mean": [{"map": ["octetTotalCount", {"select": [True]}]}]},
            {"select": [True]}
        ]}]},
        # mean (over flows) of mean (over packets) of octetTotalCount
        {"mean": [{"map": [
            {"mean": ["octetTotalCount"]},
            {"select": [True]}
        ]}]},
        # mean of octetTotalCount for all packets
        {"mean": [{"flat_map": [
            "octetTotalCount",
            {"select": [True]}
        ]}]},
        # mean of octetTotalCount for packets that have less than 1000 octetTotalCount and are in flows with less than
        #  30 packets
        {"mean": [{"flat_map": [
            # get octetTotalCount
            "octetTotalCount",
            # of packets in flows with less than 30 packets
            {"select": [{"greater": ["packetTotalCount", 30]}]},
            # only counting packets with less than 1000 octetTotalCount
            {"select": [{"less": ["octetTotalCount", 1000]}]}
        ]}]}
    ]

    Features(packet_features, 0)
    Features(flow_features, 1)
    Features(flowagg_features, 2)
