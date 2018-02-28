class Tool(object):
    def __init__(self, obj):
        self.tool = obj['tool']
        self.detail = obj['detail'] if 'detail' in obj else None
        self.availability = obj['availability']

    @property
    def name(self):
        return self.tool
