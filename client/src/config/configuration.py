class Configuration(object):

    def load(self):
        raise NotImplementedError('must define load to use this base class')

    def get(self, prop):
        raise NotImplementedError('must define get to use this base class')