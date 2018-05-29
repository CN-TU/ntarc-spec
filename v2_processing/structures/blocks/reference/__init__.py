from ... import optional


class Reference(object):
    def __init__(self, obj):
        self._author_full = obj['authors'][0]
        self.author = self._author_full
        self.title = obj['title']
        self.authors = obj['authors']
        self.publication_name = obj['publication_name']
        self.publication_type = obj['publication_type']
        self.year = obj['year']
        self.organization_publishers = optional(obj, 'organization_publishers')
        self.pages_number_of = optional(obj, 'pages_number_of')
        self.bibtex = obj['bibtex']
        self.access_open = optional(obj, 'access_open')
        self.curated_by = obj['curated_by']
        self.curated_last_revision = obj['curated_last_revision']
        self.curated_revision_number = obj['curated_revision_number']
        self._id = optional(obj, 'id')
        self._data = None

    def __repr__(self):
        return self.author + ' ' + str(self.year) + ', "' + self.title + '"'
