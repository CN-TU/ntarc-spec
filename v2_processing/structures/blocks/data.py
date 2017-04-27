from .. import optional


class Data(object):
    def __init__(self, obj):
        self.datasets = [Dataset(dd) for dd in obj['datasets']]


class Dataset(object):
    def __init__(self, obj):
        self.name = obj['dataset_name']
        self.availability = optional(obj, 'availability')
        self.format = optional(obj, 'format')
        self.types = optional(obj, 'types')
        self.generation = optional(obj, 'generation')
        self.generation_year = obj['generation_year']
        self.covered_period = optional(obj, 'covered_period')
        self.details = optional(obj, 'details')
        self.subsets = obj['subsets']
