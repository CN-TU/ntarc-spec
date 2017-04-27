from . import Reference, Data, Preprocessing, AnalysisMethod, Evaluation, Result

class FullPaper(object):
    def __init__(self, obj):
        self.reference = Reference(obj['reference'])
        self.data = Data(obj['data'])
        self.preprocessing = Preprocessing(obj['preprocessing'])
