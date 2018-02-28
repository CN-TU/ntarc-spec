from ... import Tool, optional
from .features import Features


class Preprocessing(object):
    def __init__(self, obj):
        self.performed_feature_selection = obj['performed_feature_selection']
        self.packet_analysis_oriented = obj['packet_analysis_oriented']
        self.flow_analysis_oriented = obj['flow_analysis_oriented']
        self.flow_aggregation_analysis_oriented = obj['flow_aggregation_analysis_oriented']
        self._tools = [Tool(tt) for tt in obj['tools']]
        self.normalization_type = obj['normalization_type']
        self.transformations = obj['transformations']
        self.final_data_format = obj['final_data_format']
        self._feature_selections = [FeatureSelection(ff) for ff in obj['feature_selections']] \
            if 'feature_selections' in obj else None
        self._packets = [Packet(pp) for pp in obj['packets']] if 'packets' in obj else None
        self._flows = [Flow(pp) for pp in obj['flows']] if 'flows' in obj else None
        self._flow_aggregations = [FlowAggregation(pp) for pp in obj['flow_aggregations']] \
            if 'flow_aggregations' in obj else None


class FeatureSelection(object):
    def __init__(self, obj):
        self.name = obj['name']
        self.type = optional(obj, 'type')
        self.classifier = optional(obj, 'classifier')
        self.role = optional(obj, 'role')


class Flow(object):
    def __init__(self, obj):
        self.selection = optional(obj, 'selection')
        self.role = optional(obj, 'role')
        self.main_goal = optional(obj, 'main_goal')
        self.active_timeout = optional(obj, 'active_timeout')
        self.idle_timeout = optional(obj, 'idle_timeout')
        self.bidirectional = optional(obj, 'bidirectional')

        self.features = Features(obj['features']) if 'features' in obj else None
        self.key_features = Features(obj['key_features']) if 'key_features' in obj else None


class Packet(object):
    def __init__(self, obj):
        self.selection = optional(obj, 'selection')
        self.role = optional(obj, 'role')
        self.main_goal = optional(obj, 'main_goal')
        self.features = Features(obj['features']) if 'features' in obj else None


class FlowAggregation(object):
    def __init__(self, obj):
        self.selection = optional(obj, 'selection')
        self.role = optional(obj, 'role')
        self.main_goal = optional(obj, 'main_goal')
        self.active_timeout = optional(obj, 'active_timeout')

        self.features = Features(obj['features']) if 'features' in obj else None
        self.key_features = Features(obj['key_features']) if 'key_features' in obj else None

    @property
    def bidirectional(self):
        return None
