from .. import Tool, optional


class AnalysisMethod(object):
    def __init__(self, obj):
        self.supervised_learning = obj['supervised_learning']
        self.unsupervised_learning = obj['unsupervised_learning']
        self.semisupervised_learning = obj['semisupervised_learning']
        self.anomaly_detection = obj['anomaly_detection']
        self.tools = [Tool(tt) for tt in obj['tools']]
        self.algorithms = [Algorithm(aa) for aa in obj['algorithms']] if 'algorithms' in obj else None


class Algorithm(object):
    def __init__(self, obj):
        self.name = obj['name']
        self.subname = optional(obj, 'subname')
        self.learning = optional(obj, 'learning')
        self.role = optional(obj, 'role')
        self.metric = optional(obj, 'metric/decision_criteria')
        self.tools = [Tool(tt) for tt in obj['tools']] if 'tools' in obj else None
        self.source = optional(obj, 'source')
        self.parameters_provided = optional(obj, 'parameters_provided')

    @property
    def decision_criteria(self):
        return self.metric

    @property
    def metric_decision_criteria(self):
        return self.metric
