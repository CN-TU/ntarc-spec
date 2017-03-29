import csv
from itertools import combinations
from os.path import expanduser

from analyze import *
from analyze import _iterate_directory
from conf import PROJECT_PATH
from structures.high_level import Dataset
from structures.metadata import Reference

PAPERS_DIR = PROJECT_PATH + '/papers'
HOME = expanduser("~")


class PaperNode(object):
    def __init__(self, id, title, year, author, done, afil):
        self.id = id
        self.title = title
        self.year = year
        self.author = author
        self.done = done
        self.afil = afil

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return [self.id, self.title, self.year, self.author, self.done, self.afil]


class AffiliationNode(object):
    def __init__(self, id, name, done, location):
        self.id = id
        self.name = name
        self.done = done
        self.location = location

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return [self.id, self.name, self.done, self.location[0], self.location[1]]


def get_papers_graph():
    nodes = set()
    edges = list()
    for pap in list_references(PAPERS_DIR):
        try:
            afil = pap.affiliations[0].data['DAfN']
        except IndexError:
            afil = ''
        node_a = PaperNode(pap.id, pap.title, pap.year, pap.author, 1, afil)
        print('paper:', pap.title)
        nodes.add(node_a)
    for pap in list_references(PAPERS_DIR):
        if len(pap.bibliography) == 0:
            print('PROBLEM:', pap.title, pap.year)
        for c in pap.bibliography:
            try:
                afil = c.affiliations[0].data['DAfN']
            except:
                afil = ''
            node_b = PaperNode(c.id, c.title, c.year, c.author, 0, afil)
            nodes.add(node_b)
            edge = [pap.id, c.id, 1.]
            edges.append(edge)

    return nodes, edges


def get_affiliations_graph():
    nodes = set()
    edges = {}
    for pap in list_references(PAPERS_DIR):
        print('paper:', pap.title)
        affils = pap.affiliations
        for affil in affils:
            nodes.add(AffiliationNode(affil.id, affil.data['DAfN'], 1, affil.location))
    for pap in list_references(PAPERS_DIR):
        affils = pap.affiliations
        if len(pap.bibliography) == 0:
            print('PROBLEM:', pap.title, pap.year)
        for c in pap.bibliography:
            new_affils = c.affiliations
            for new_affil in new_affils:
                try:
                    nodes.add(AffiliationNode(new_affil.id, new_affil.data['DAfN'], 0, new_affil.location))
                except IndexError:
                    raise IndexError(c.title)
            for a in affils:
                for aa in new_affils:
                    if (a, aa) in edges:
                        edges[a.id, aa.id] += 1.
                    else:
                        edges[a.id, aa.id] = 1.
    out_edges = []
    for (source, target), weight in edges.items():
        out_edges.append([source, target, weight])
    return nodes, out_edges


def get_affiliations_collab_graph():
    nodes = set()
    edges = {}
    for pap in list_references(PAPERS_DIR):
        print('paper:', pap.title)
        affils = pap.affiliations
        for affil in affils:
            nodes.add(AffiliationNode(affil.id, affil.data['DAfN'], 1, affil.location))
        for a1, a2 in combinations(affils, 2):
            aff1 = a1.id
            aff2 = a2.id
            if (aff1, aff2) in edges:
                edges[aff1, aff2] += 1.
            else:
                edges[aff1, aff2] = 1.
    out_edges = []
    for (source, target), weight in edges.items():
        out_edges.append([source, target, weight, 'Undirected'])
    return nodes, out_edges


def get_affiliations_collab_graph():
    """
    Gets usage of public datasets for affiliations
    """
    nodes = {}
    edges = {}
    for d in _iterate_directory(PAPERS_DIR):
        pap = Reference(d)
        has_public = False
        if 'datasets' in d and d['datasets'] is not None:
            for dd in d['datasets']:
                dataset = Dataset(dd)
                if dataset.availability == 'public':
                    has_public = True

        print('paper:', pap.title)
        affils = pap.affiliations
        for affil in affils:
            if affil.id in nodes:
                tup = nodes[affil.id]
                new_tup = (tup[0], tup[1], tup[2], tup[3],
                           tup[4], tup[5] + int(has_public), tup[6] + 1)
                nodes[affil.id] = new_tup
            else:
                nodes[affil.id] = (affil.id, affil.data['DAfN'], 1, affil.location[0],
                                   affil.location[1], int(has_public), 1)
        for a1, a2 in combinations(set(affils), 2):
            aff1 = min(a1.id, a2.id)
            aff2 = max(a1.id, a2.id)
            if (aff1, aff2) in edges:
                edges[aff1, aff2] += 1.
            else:
                edges[aff1, aff2] = 1.
    out_nodes = []
    for key, val in nodes.items():
        tup = (val[0], val[1], val[2], val[3],
               val[4], float(val[5]) / val[6], val[6])
        out_nodes.append(tup)

    out_edges = []
    for (source, target), weight in edges.items():
        out_edges.append([source, target, weight, 'Undirected'])
    return out_nodes, out_edges


def get_affiliations_collab_graph():
    """
    Gets usage of feature selection methods for affiliations
    """
    nodes = {}
    edges = {}
    for d in _iterate_directory(PAPERS_DIR):
        pap = Reference(d)
        has_feat_sel = False
        if 'methods' in d and d['methods'] is not None:
            for dd in d['methods']:
                if dd['type'] == 'feature_selection':
                    has_feat_sel = True

        print('paper:', pap.title)
        affils = pap.affiliations
        for affil in affils:
            if affil.id in nodes:
                tup = nodes[affil.id]
                new_tup = (tup[0], tup[1], tup[2], tup[3],
                           tup[4], tup[5] + int(has_feat_sel), tup[6] + 1)
                nodes[affil.id] = new_tup
            else:
                nodes[affil.id] = (affil.id, affil.data['DAfN'], 1, affil.location[0],
                                   affil.location[1], int(has_feat_sel), 1)
        for a1, a2 in combinations(set(affils), 2):
            aff1 = min(a1.id, a2.id)
            aff2 = max(a1.id, a2.id)
            if (aff1, aff2) in edges:
                edges[aff1, aff2] += 1.
            else:
                edges[aff1, aff2] = 1.
    out_nodes = []
    for key, val in nodes.items():
        tup = (val[0], val[1], val[2], val[3],
               val[4], float(val[5]) / val[6], val[6])
        out_nodes.append(tup)

    out_edges = []
    for (source, target), weight in edges.items():
        out_edges.append([source, target, weight, 'Undirected'])
    return out_nodes, out_edges




nodes, edges = get_affiliations_collab_graph()
with open(HOME + '/nodes.csv', 'w') as fd:
    writer = csv.writer(fd)
    # writer.writerow(['Id', 'Label', 'Year', 'Author', 'Done', 'Affiliation'])
    writer.writerow(['Id', 'Label', 'Done', 'lat', 'lng', 'feature_selection', 'paper_count'])
    for node in nodes:
        n = node.__repr__()
        n = node
        writer.writerow(n)

with open(HOME + '/edges.csv', 'w') as fd:
    writer = csv.writer(fd)
    # writer.writerow(['Source', 'Target', 'Weight'])
    writer.writerow(['Source', 'Target', 'Weight', 'Type'])
    for edge in edges:
        writer.writerow(edge)
