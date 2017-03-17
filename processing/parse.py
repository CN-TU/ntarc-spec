import os
import traceback
from collections import OrderedDict
import simplejson
from structures import Reference, Feature


def _discounted_citations(ref):
    return ref.citations / (2017 - ref.year)**1.5 if ref.citations > 0 else 0


def _find_all(d, tag):
    if isinstance(d, dict):
        for k, v in d.items():
            if k == tag and v is not None:
                yield {k: v}
            elif isinstance(v, dict):
                for id_val in _find_all(v, tag):
                    yield id_val
            elif isinstance(v, list):
                for val in v:
                    for id_val in _find_all(val, tag):
                        yield id_val


def _get_existing_types(d):
    possible_types = ['flows', 'packets', 'aggregated']
    return [t for t in possible_types if t in d and d[t] is not None]


def _open_json(filename):
    try:
        return simplejson.load(open(filename))
    except:
        print(filename)
        traceback.print_exc()


def _iterate_directory(directory):
    for year in sorted(os.listdir(directory)):
        for filename in sorted(os.listdir(directory + os.sep + year)):
            if filename[-5:] == '.json':
                yield _open_json(directory + os.sep + year + os.sep + filename)


##############################################
#
# List things...
#
##############################################


def find_all_features(d):
    out = set()
    for feats in _find_all(d, "features"):
        out.update(*Feature(feats).get_features())
    return out


def find_flow_features(d):
    out = set()
    if d['flows'] is not None:
        for flow in d['flows']:
            feats = flow['features']
            if feats is not None:
                out.update(*Feature({'features': feats}).get_features())
    return out


def find_all_operations(d):
    out = set()
    for feats in _find_all(d, "features"):
        out.update(Feature(feats).get_operations())
    return out


def list_goals(directory):
    out = set()
    for d in _iterate_directory(directory):
        for t in _get_existing_types(d):
            for info in d[t]:
                try:
                    out.update(set(info['goals']))
                except KeyError:
                    continue
    return out


def list_flow_goals(directory):
    out = set()
    for d in _iterate_directory(directory):
        if d['flows'] is not None and len(d['flows']) > 0:
            for t in _get_existing_types(d):
                for info in d[t]:
                    try:
                        out.update(set(info['goals']))
                    except KeyError:
                        continue
    return out


def list_features(directory):
    out = set()
    for d in _iterate_directory(directory):
        out.update(find_all_features(d))
    return out


def list_flow_features(directory):
    out = set()
    for d in _iterate_directory(directory):
        out.update(find_flow_features(d))
    return out


def list_operations(directory):
    out = set()
    for d in _iterate_directory(directory):
        out.update(find_all_operations(d))
    return out


def list_references(directory):
    out = []
    for d in _iterate_directory(directory):
        out.append(Reference(d))
    return out


def list_flow_references(directory):
    out = []
    for d in _iterate_directory(directory):
        if d['flows'] is not None and len(d['flows']) > 0:
            out.append(Reference(d))
    return out


##############################################
#
# Goals to...
#
##############################################


def goals_to_features(directory, invert=False):
    out = {}
    for d in _iterate_directory(directory):
        for t in _get_existing_types(d):
            for info in d[t]:
                try:
                    goals = info['goals']
                except KeyError:
                    continue
                if invert:
                    for feat in find_all_features(info):
                        if feat not in out:
                            out[feat] = set()
                        out[feat].update(set(goals))
                else:
                    for goal in goals:
                        if goal not in out:
                            out[goal] = set()
                        out[goal].update(find_all_features(info))
    return out


def goals_to_feature_usage(directory):
    out = {}
    for d in _iterate_directory(directory):
        for t in _get_existing_types(d):
            for info in d[t]:
                try:
                    goals = info['goals']
                except KeyError:
                    continue
                for goal in goals:
                    if goal not in out:
                        out[goal] = {'TOTAL': 0}
                    out[goal]['TOTAL'] += 1
                    for feat in find_all_features(info):
                        if feat not in out[goal]:
                            out[goal][feat] = 0
                        out[goal][feat] += 1
    return out


##############################################
#
# Features to...
#
##############################################


def features_to_citations(directory):
    out = {}
    for d in _iterate_directory(directory):
        ref = Reference(d)
        for feat in find_all_features(d):
            if feat not in out:
                out[feat] = 0
            out[feat] += ref.citations
    return out


def features_to_discounted_citations(directory):
    out = {}
    for d in _iterate_directory(directory):
        ref = Reference(d)
        for feat in find_all_features(d):
            if feat not in out:
                out[feat] = 0
            out[feat] += _discounted_citations(ref)
    return out


def features_to_avg_citations(directory):
    cits = features_to_citations(directory)
    paper_counts = features_to_nr_of_papers(directory)

    out = {}
    for key in cits:
        out[key] = cits[key] / paper_counts[key]
    return out


def features_to_avg_discounted_citations(directory):
    cits = features_to_discounted_citations(directory)
    paper_counts = features_to_nr_of_papers(directory)

    out = {}
    for key in cits:
        out[key] = cits[key] / paper_counts[key]
    return out


def features_to_authors(directory):
    out = {}
    for d in _iterate_directory(directory):
        ref = Reference(d)
        for feat in find_all_features(d):
            if feat not in out:
                out[feat] = []
            out[feat].append(ref.author + ' ' + str(ref.year))
    return out


def features_to_references(directory):
    out = {}
    for d in _iterate_directory(directory):
        ref = Reference(d)
        for feat in find_all_features(d):
            if feat not in out:
                out[feat] = []
            out[feat].append(ref)
    return out


def features_to_nr_of_papers(directory):
    out = {}
    for d in _iterate_directory(directory):
        for feat in find_all_features(d):
            if feat not in out:
                out[feat] = 0
            out[feat] += 1
    return out


def features_to_year_frequency(directory):
    out = {}
    for d in _iterate_directory(directory):
        ref = Reference(d)
        for feat in find_all_features(d):
            if feat not in out:
                out[feat] = OrderedDict((k, 0) for k in range(2000, 2017))
            out[feat][ref.year] += 1
    return out


_features_computables = ['nr_of_papers', 'citations', 'discounted_citations', 'avg_citations',
                         'avg_discounted_citations',
                         'authors', 'year_frequency']


def features_to_all(directory):
    values = {}
    for k in _features_computables:
        values[k] = (eval('features_to_' + k + '("' + directory + '")'))

    out = []
    for feat in list_features(directory):
        d = OrderedDict()
        d['feature'] = feat
        for k in _features_computables:
            d[k] = values[k][feat]
        out.append(d)
    return out


##############################################
#
# Operations to...
#
##############################################


def operations_to_citations(directory):
    out = {}
    for d in _iterate_directory(directory):
        ref = Reference(d)
        for op in find_all_operations(d):
            if op not in out:
                out[op] = 0
            out[op] += ref.citations
    return out


def operations_to_features(directory):
    out = {}
    for d in _iterate_directory(directory):
        for op in find_all_operations(d):
            if op not in out:
                out[op] = []
            for f in _find_all(d, 'features'):
                out[op].append(f)
    return out


def operations_to_year_frequency(directory):
    out = {}
    for d in _iterate_directory(directory):
        ref = Reference(d)
        for op in find_all_operations(d):
            if op not in out:
                out[op] = OrderedDict((k, 0) for k in range(2000, 2017))
            out[op][ref.year] += 1
    return out


##############################################
#
# Flow features to...
#
##############################################


def flow_features_to_citations(directory):
    out = {}
    for d in _iterate_directory(directory):
        ref = Reference(d)
        for feat in find_flow_features(d):
            if feat not in out:
                out[feat] = 0
            out[feat] += ref.citations
    return out


def flow_features_to_discounted_citations(directory):
    out = {}
    for d in _iterate_directory(directory):
        ref = Reference(d)
        for feat in find_flow_features(d):
            if feat not in out:
                out[feat] = 0
            out[feat] += _discounted_citations(ref)
    return out


def flow_features_to_avg_citations(directory):
    cits = flow_features_to_citations(directory)
    paper_counts = flow_features_to_nr_of_papers(directory)

    out = {}
    for key in cits:
        out[key] = cits[key] / paper_counts[key]
    return out


def flow_features_to_avg_discounted_citations(directory):
    cits = flow_features_to_discounted_citations(directory)
    paper_counts = flow_features_to_nr_of_papers(directory)

    out = {}
    for key in cits:
        out[key] = cits[key] / paper_counts[key]
    return out


def flow_features_to_authors(directory):
    out = {}
    for d in _iterate_directory(directory):
        ref = Reference(d)
        for feat in find_flow_features(d):
            if feat not in out:
                out[feat] = []
            out[feat].append(ref.author + ' ' + str(ref.year))
    return out


def flow_features_to_references(directory):
    out = {}
    for d in _iterate_directory(directory):
        ref = Reference(d)
        for feat in find_flow_features(d):
            if feat not in out:
                out[feat] = []
            out[feat].append(ref)
    return out


def flow_features_to_nr_of_papers(directory):
    out = {}
    for d in _iterate_directory(directory):
        for feat in find_flow_features(d):
            if feat not in out:
                out[feat] = 0
            out[feat] += 1
    return out


def flow_features_to_year_frequency(directory):
    out = {}
    for d in _iterate_directory(directory):
        ref = Reference(d)
        for feat in find_flow_features(d):
            if feat not in out:
                out[feat] = OrderedDict((k, 0) for k in range(2000, 2017))
            out[feat][ref.year] += 1
    return out


_flow_features_computables = ['nr_of_papers', 'citations', 'discounted_citations', 'avg_citations',
                         'avg_discounted_citations',
                         'authors', 'year_frequency']


def flow_features_to_all(directory):
    values = {}
    for k in _features_computables:
        values[k] = (eval('flow_features_to_' + k + '("' + directory + '")'))

    out = []
    for feat in list_flow_features(directory):
        d = OrderedDict()
        d['feature'] = feat
        for k in _features_computables:
            d[k] = values[k][feat]
        out.append(d)
    return out
