from .. import optional

class Result(object):
    def __init__(self, obj):
        self.main_goal = obj['main_goal']
        self.subgoals = optional(obj, 'subgoals')
        self.focus_main = obj['focus_main']
        self.claimed_improvements = obj['claimed_improvements']
        self.reproducibility = optional(obj, 'reproducibility')
