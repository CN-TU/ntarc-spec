import json
import os
import time
import requests
import six
from googleplaces import GooglePlaces
from . import PROJECT_PATH, API_KEY, MAPS_API_KEY
from structures.high_level import Flow, Packet, FlowAggregation, Method, Evaluation, Dataset


CACHE_DIR = PROJECT_PATH + '/processing/.cache'


class BaseEntity(object):
    url_base = 'https://westus.api.cognitive.microsoft.com/academic/v1.0/evaluate'
    api_key = API_KEY
    attrs = None

    def __init__(self, id):
        self._id = id
        self._data = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

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
            json.dump(data, fd)

    def _load_cache(self):
        with open(self._cache_id_filename, 'r') as fd:
            self._data = json.load(fd)

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

    @property
    def _cache_location_filename(self):
        return CACHE_DIR + os.sep + 'affiliation_location' + os.sep + str(self._id)

    @property
    def location(self):
        if '_location_info' not in self.__dict__:
            self._query_location()
        return self._get_location()

    def _get_location(self):
        return (
            float(self._location_info['geometry']['location']['lat']),
            float(self._location_info['geometry']['location']['lng'])
        )

    def _check_location_cache(self):
        return os.path.isfile(self._cache_location_filename)

    def _query_location(self):
        if not self._check_location_cache():
            google_places = GooglePlaces(MAPS_API_KEY)
            query_result = google_places.text_search(self.data['DAfN'])
            try:
                self._location_info = query_result.raw_response['results'][0]
            except IndexError:
                print(query_result.raw_response)
                raise IndexError(self.id)
            self._write_location_cache(self._location_info)
            time.sleep(1)
        else:
            self._load_location_cache()

    def _load_location_cache(self):
        with open(self._cache_location_filename, 'r') as fd:
            self._location_info = json.load(fd)

    def _write_location_cache(self, location_info):
        with open(self._cache_location_filename, 'w') as fd:
            json.dump(location_info, fd)


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
                d = json.load(open(d, 'r'))
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


class MetaPaper(object):
    def __init__(self, d):
        if 'reference' in d and d['reference'] is not None:
            self.reference = Reference(d['reference'])
        else:
            raise ValueError('No reference found!')

        self.packets = [Packet(p) for p in _get_list(d, 'packets')]
        self.flows = [Flow(f) for f in _get_list(d, 'flows')]
        self.flow_aggregations = [FlowAggregation(f) for f in _get_list(d, 'flow_aggregations')]
        self.datasets = [Dataset(dd) for dd in _get_list(d, 'datasets')]
        self.evaluations = [Evaluation(e) for e in _get_list(d, 'evaluations')]
        self.methods = [Method(m) for m in _get_list(d, 'methods')]


def _get_list(d, key):
    if key in d and d[key] is not None and len(d[key]) > 0:
        if type(d[key]) is list:
            return d[key]
        raise ValueError(key + ' must be a list (or null)!')
    return []