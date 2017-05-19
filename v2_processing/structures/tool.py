class Tool(object):
    def __init__(self, obj):
        self.tool = obj['tool']
        self.detail = obj['tool'] if 'tool' in obj else None
        self.availability = obj['availability']
