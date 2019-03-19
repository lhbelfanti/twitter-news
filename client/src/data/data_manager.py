from di import Injectable


class DataManager(Injectable):
    def __init__(self):
        super().__init__()

    def set_trending_topics(self, data):
        raise NotImplementedError('must define set_trending_topics to use this base class')

    def get_trending_topics(self):
        raise NotImplementedError('must define get_trending_topics to use this base class')

    def define_dependencies(self):
        raise NotImplementedError('must define define_dependencies to use this base class')

    def construct(self, dependencies):
        raise NotImplementedError('must define construct to use this base class')
