import json
import os
import time
import requests
import six
from ... import CACHE_DIR, optional
from .metadata import BaseEntity, Affiliation


class Reference(BaseEntity):
    attrs = 'Id,Ti,L,Y,D,CC,ECC,AA.AuN,AA.AuId,AA.AfN,AA.AfId,F.FN,F.FId,J.JN,J.JId,C.CN,C.CId,RId,W,E'

    def __init__(self, obj):
        if isinstance(obj, six.integer_types):
            self._id = obj
            self._author = None
            self._title = None
            self._year = None
            self._data = None
            self._query_id(obj)
        else:
            self._author_full = obj['authors'][0]
            self._author = self._author_full
            self._title = obj['title']
            self.publication_name = obj['publication_name']
            self.publication_type = obj['publication_type']
            self._year = obj['year']
            self.organization_publishers = optional(obj, 'organization_publishers')
            self.pages_number_of = optional(obj, 'pages_number_of')
            self.bibtex = obj['bibtex']
            self.access_open = optional(obj, 'access_open')
            self.curated_by = obj['curated_by']
            self.curated_last_revision = obj['curated_last_revision']
            self.curated_revision_number = obj['curated_revision_number']
            self._id = optional(obj, 'id')
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
            json.dump(data, fd)

    def _load_cache(self):
        try:
            with open(self._cache_filename, 'r') as fd:
                id = int(fd.read())
        except:
            id = self._id
        with open(self.get_cache_filename(id), 'r') as fd:
            self._data = json.load(fd)

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
