from ... import Tool, optional
from .features import Features


class Preprocessing(object):
    def __init__(self, obj):
        self.performed_feature_selection = obj['performed_feature_selection']
        self.packet_analysis_oriented = obj['packet_analysis_oriented']
        self.flow_analysis_oriented = obj['flow_analysis_oriented']
        self.flow_aggregation_analysis_oriented = obj['flow_aggregation_analysis_oriented']
        self._tools = [Tool(tt) for tt in obj['tools']] \
            if obj['tools'] not in ['missing', 'none'] else []
        self.normalization_type = obj['normalization_type']
        self.transformations = obj['transformations']
        self.final_data_format = obj['final_data_format']
        self._feature_selections = [FeatureSelection(ff) for ff in obj['feature_selections']] \
            if 'feature_selections' in obj and obj['feature_selections'] != 'none' else None
        self._packets = [Packet(pp) for pp in obj['packets']] \
            if 'packets' in obj and obj['packets'] != 'none' else None
        self._flows = [Flow(pp) for pp in obj['flows']] \
            if 'flows' in obj and obj['flows'] != 'none' else None
        self._flow_aggregations = [FlowAggregation(pp) for pp in obj['flow_aggregations']] \
            if 'flow_aggregations' in obj and obj['flow_aggregations'] != 'none' else None

    @property
    def tools(self):
        return self._tools

    @property
    def feature_selections(self):
        return self._feature_selections

    @property
    def packets(self):
        return self._packets

    @property
    def flows(self):
        return self._flows

    @property
    def flow_aggregations(self):
        return self._flow_aggregations


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

        self.features = Features(obj['features'], level=1) \
            if 'features' in obj and obj['features'] not in ['missing', 'none'] else None
        self.key_features = Features(obj['key_features'], level=1) \
            if 'key_features' in obj and obj['key_features'] not in ['missing', 'none'] else None


class Packet(object):
    def __init__(self, obj):
        self.selection = optional(obj, 'selection')
        self.role = optional(obj, 'role')
        self.main_goal = optional(obj, 'main_goal')
        self.features = Features(obj['features'], level=0) \
            if 'features' in obj and obj['features'] not in ['missing', 'none'] else None


class FlowAggregation(object):
    def __init__(self, obj):
        self.selection = optional(obj, 'selection')
        self.role = optional(obj, 'role')
        self.main_goal = optional(obj, 'main_goal')
        self.active_timeout = optional(obj, 'active_timeout')
        self.bidirectional = optional(obj, 'bidirectional')

        self.features = Features(obj['features'], level=2) \
            if 'features' in obj and obj['features'] not in ['missing', 'none'] else None
        self.key_features = Features(obj['key_features'], level=2) \
            if 'key_features' in obj and obj['key_features'] not in ['missing', 'none'] else None
