import time
import six
import csv
import xml.etree.cElementTree as ElementTree
from utils import XmlDictConfig
from structures import Reference
from conf import PROJECT_PATH


META_FILE = PROJECT_PATH + '/papers_list.xml'
OUTPUT_CSV = PROJECT_PATH + '/papers_list.csv'


class Paper(Reference):
    def __init__(self, paper):
        self.title = paper['titles']['title']
        self._author_full = paper['contributors']['authors']['author']
        if isinstance(self._author_full, six.string_types):
            self._author_full = [self._author_full]
        self.author = self._author_full[0].split(',')[0]
        self.year = int(paper['dates']['year'])
        self._data = None


tree = ElementTree.parse(META_FILE)
root = tree.getroot()
xmldict = XmlDictConfig(root)

papers = xmldict['records']['record']

time.sleep(1)
url_base = 'https://vs.cn.tuwien.ac.at/cn/phd-df/bibliography/'

with open(OUTPUT_CSV, 'w') as fd:
    writer = csv.writer(fd, delimiter=',')
    writer.writerow(["Title", "Authors", "Year", "Notes", "Citations", "Url"])
    for paper in papers:
        p = Paper(paper)

        title = p.title
        print(title)
        authors = '; '.join(p._author_full)
        year = p.year
        notes = paper['notes']
        url = url_base + paper['urls']['pdf-urls']['url'].split('-pdf://')[1]

        try:
            citations = p.citations
        except IndexError:
            writer.writerow([title, authors, year, notes, -1, url])
        else:
            writer.writerow([title, authors, year, notes, citations, url])

        # time.sleep(2)

pass
