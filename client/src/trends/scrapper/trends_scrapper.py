from di import Injectable


class TrendsScrapper(Injectable):
    def __init__(self):
        super().__init__()

    def get_trends_data(self):
        raise NotImplementedError('must define get_trends_data to use this base class')

    def define_dependencies(self):
        raise NotImplementedError('must define define_dependencies to use this base class')

    def construct(self, dependencies):
        raise NotImplementedError('must define construct to use this base class')
