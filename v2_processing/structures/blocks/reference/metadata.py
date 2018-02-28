import simplejson as json
import os
import time
import requests
try:
    from googleplaces import GooglePlaces
except ImportError:
    GooglePlaces = None
from ... import API_KEY, MAPS_API_KEY, CACHE_DIR


class BaseEntity(object):
    _url_base = 'https://westus.api.cognitive.microsoft.com/academic/v1.0/evaluate'
    _api_key = API_KEY
    _attrs = None

    def __init__(self, id):
        self._id = id
        self._data = None

    def __hash__(self):
        try:
            return hash(self.id)
        except AttributeError:
            return hash(str(self))

    def __eq__(self, other):
        try:
            return self.id == other.id
        except AttributeError:
            return str(self) == str(other)

    def _query_id_attrs(self, id, attrs):
        if not self._check_cache():
            expr = 'Id=' + str(id)

            url = self._url_base
            url += '?expr=' + expr
            url += '&attributes=' + attrs

            r = requests.get(url, headers={'Ocp-Apim-Subscription-Key': self._api_key})
            data = r.json()
            if self._data is None:
                self._data = {}
            self._data['microsoft_api'] = data['entities'][0]
            self._write_cache(self._data)
            time.sleep(1)
        else:
            self._load_cache()

    @property
    def id(self):
        if CACHE_DIR is not None and API_KEY is not None and len(API_KEY) > 0:
            return self._saved_data['microsoft_api']['Id']
        else:
            raise AttributeError('Asked for ID, but provided no cache directory or API key.')

    @property
    def _saved_data(self):
        if self._data is None:
            self._query_id_attrs(self._id, self._attrs)
        return self._data

    def _check_cache(self):
        return os.path.isfile(self._cache_id_filename)

    @property
    def _cache_id_filename(self):
        raise NotImplementedError

    def _write_cache(self, data):
        try:
            with open(self._cache_id_filename, 'r') as fd:
                old_data = json.load(fd)
                old_data.update(data)
                data = old_data
        except FileNotFoundError:
            pass
        with open(self._cache_id_filename, 'w') as fd:
            json.dump(data, fd)

    def _load_cache(self):
        with open(self._cache_id_filename, 'r') as fd:
            self._data = json.load(fd)

    def _query_id(self, id):
        self._query_id_attrs(id, self._attrs)


class Author(BaseEntity):
    _attrs = 'Id,AuN,DAuN,CC,ECC,E,SSD'

    @property
    def _cache_id_filename(self):
        dirname = CACHE_DIR + os.sep + 'author_id'
        os.makedirs(dirname, exist_ok=True)
        return dirname + os.sep + str(self._id)


class Affiliation(BaseEntity):
    _attrs = 'Id,AfN,DAfN,CC,ECC,SSD'

    @property
    def _cache_id_filename(self):
        dirname = CACHE_DIR + os.sep + 'affiliation_id'
        os.makedirs(dirname, exist_ok=True)
        return dirname + os.sep + str(self._id)

    @property
    def _cache_location_filename(self):
        dirname = CACHE_DIR + os.sep + 'affiliation_location'
        os.makedirs(dirname, exist_ok=True)
        return dirname + os.sep + str(self._id)

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
            query_result = google_places.text_search(self._saved_data['microsoft_api']['DAfN'])
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

    @property
    def name(self):
        return self._saved_data['microsoft_api']['DAfN']


class Journal(BaseEntity):
    _attrs = 'Id,DJN,JN,CC,ECC,SSD'

    @property
    def _cache_id_filename(self):
        dirname = CACHE_DIR + os.sep + 'journal_id'
        os.makedirs(dirname, exist_ok=True)
        return dirname + os.sep + str(self._id)


class ConferenceSeries(BaseEntity):
    _attrs = 'Id,CN,DCN,CC,ECC,F.FId,F.FN,SSD'

    @property
    def _cache_id_filename(self):
        dirname = CACHE_DIR + os.sep + 'conferenceseries_id'
        os.makedirs(dirname, exist_ok=True)
        return dirname + os.sep + str(self._id)


class ConferenceInstance(BaseEntity):
    _attrs = 'Id,CIN,DCN,CIL,CISD,CIED,CIARD,CISDD,CIFVD,CINDD,CD.T,CD.D,PCS.CN,PCS.CId,CC,ECC,SSD'

    @property
    def _cache_id_filename(self):
        dirname = CACHE_DIR + os.sep + 'conferenceinstance_id'
        os.makedirs(dirname, exist_ok=True)
        return dirname + os.sep + str(self._id)


class FieldOfStudy(BaseEntity):
    _attrs = 'Id,FN,DFN,CC,ECC,FL,FP.FN,FP.FId,SSD'

    @property
    def _cache_id_filename(self):
        dirname = CACHE_DIR + os.sep + 'fieldofstudy_id'
        os.makedirs(dirname, exist_ok=True)
        return dirname + os.sep + str(self._id)


def _get_list(d, key):
    if key in d and d[key] is not None and len(d[key]) > 0:
        if type(d[key]) is list:
            return d[key]
        raise ValueError(key + ' must be a list (or null)!')
    return []