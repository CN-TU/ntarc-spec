from ...structures import optional


class Evaluation(object):
    def __init__(self, obj):
        self.algorithm_comparison = obj['algorithm_comparison']
        self.internal_validation = obj['internal_validation']
        self.external_validation = obj['external_validation']
        self.dpi_based_validation = obj['dpi-based_validation']
        self.port_based_validation = obj['port-based_validation']
        self.pre_knowledge_based_validation = obj['pre-knowledge-based_validation']
        self.manual_verification = obj['manual_verification']
        self.implementation_in_real_scenario = obj['implementation_in_real_scenario']
        self.train_test_separation = obj['train_test_separation']
        self.methods = [EvaluationMethod(mm) for mm in obj['methods']] if 'methods' in obj else None


class EvaluationMethod(object):
    def __init__(self, obj):
        self.name = obj['name']
        self.type = optional(obj, 'type')
        self.metrics = optional(obj, 'metrics')
        self.source = optional(obj, 'source')
