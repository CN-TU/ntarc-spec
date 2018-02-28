import os
import json
from . import Reference, Data, Preprocessing, AnalysisMethod, Evaluation, Result


def _get_public_variables(obj):
    return {name: getattr(obj, name) for name in dir(obj) if not name.startswith("_")}


class FullPaper(Reference):
    _attrs = 'Id,Ti,L,Y,D,CC,ECC,AA.AuN,AA.AuId,AA.AfN,AA.AfId,F.FN,F.FId,J.JN,J.JId,C.CN,C.CId,RId,W,E'

    def __init__(self, obj):
        self._complete_obj = obj
        self.reference_block = Reference(obj['reference'])
        self.data_block = Data(obj['data'])
        self.preprocessing_block = Preprocessing(obj['preprocessing'])
        self.analysis_method_block = AnalysisMethod(obj['analysis_method'])
        self.evaluation_block = Evaluation(obj['evaluation'])
        self.result_block = Result(obj['results'])

        self._data = None

    def _write_cache(self, data):
        try:
            with open(self._cache_id_filename, 'r') as fd:
                old_data = json.load(fd)
                old_data.update(data)
                data = old_data
        except FileNotFoundError:
            pass
        with open(self._cache_filename, 'w') as fd:
            fd.write(str(self.id))

        data['reference'] = _get_public_variables(self.reference_block)
        data['data'] = [_get_public_variables(dd) for dd in self.data_block.datasets]
        data['preprocessing'] = _get_public_variables(self.preprocessing_block)
        with open(self._cache_id_filename, 'w') as fd:
            json.dump(data, fd)

    @property
    def reference(self):
        return self.reference_block

    @property
    def data(self):
        return self.data_block

    @property
    def preprocessing(self):
        return self.preprocessing_block

    @property
    def analysis_method(self):
        return self.analysis_method_block

    @property
    def evaluation(self):
        return self.evaluation_block

    @property
    def result(self):
        return self.result_block

    @property
    def title(self):
        return self.reference_block.title

    @property
    def _saved_data(self):
        if self._data is None:
            self._query()
        return self._data

    def _check_cache(self):
        if os.path.isfile(self._cache_filename):
            id_file = self._cache_filename + '/../' + open(self._cache_filename).read()
            return os.path.isfile(id_file)
        return False

    @property
    def author(self):
        return self.reference_block.author

    @property
    def title(self):
        return self.reference_block.title

    @property
    def year(self):
        return self.reference_block.year
