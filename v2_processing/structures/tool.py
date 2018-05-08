class Tool(object):
    def __init__(self, obj):
        self.name = obj['name']
        self.detail = obj['detail'] if 'detail' in obj else None
        self.availability = obj['availability']
