from os.path import expanduser
import csv
from parse import *
from conf import PROJECT_PATH


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
                nodes.add(AffiliationNode(new_affil.id, new_affil.data['DAfN'], 0, new_affil.location))
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



nodes, edges = get_affiliations_graph()
with open(HOME + '/nodes.csv', 'w') as fd:
    writer = csv.writer(fd)
    # writer.writerow(['Id', 'Title', 'Year', 'Author', 'Done', 'Affiliation'])
    writer.writerow(['Id', 'Name', 'Done', 'Latitude', 'Longitude'])
    for node in nodes:
        n = node.__repr__()
        writer.writerow(n)

with open(HOME + '/edges.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['Source', 'Target', 'Weight'])
    for edge in edges:
        writer.writerow(edge)
