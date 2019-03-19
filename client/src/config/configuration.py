from di import Injectable


class Configuration(Injectable):
    def __init__(self):
        super().__init__()

    def load(self):
        raise NotImplementedError('must define load to use this base class')

    def get(self, prop):
        raise NotImplementedError('must define get to use this base class')

    def define_dependencies(self):
        raise NotImplementedError('must define define_dependencies to use this base class')

    def construct(self, dependencies):
        raise NotImplementedError('must define construct to use this base class')
