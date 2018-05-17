import os
import json
from . import Reference, Data, Preprocessing, AnalysisMethod, Evaluation, Result


def _get_public_variables(obj):
    return {name: getattr(obj, name) for name in dir(obj) if not name.startswith("_")}


class FullPaper(object):
    def __init__(self, obj):
        self._complete_obj = obj
        self.reference_block = Reference(obj['reference'])
        self.data_block = Data(obj['data'])
        self.preprocessing_block = Preprocessing(obj['preprocessing'])
        self.analysis_method_block = AnalysisMethod(obj['analysis_method'])
        self.evaluation_block = Evaluation(obj['evaluation'])
        self.result_block = Result(obj['result'])

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
    def author(self):
        return self.reference_block.author

    @property
    def year(self):
        return self.reference_block.year
