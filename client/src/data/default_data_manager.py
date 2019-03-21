from data import DataManager


class DefaultDataManager(DataManager):
    def __init__(self):
        super().__init__()
        self._trending_topics = None

    def _define_dependencies(self):
        pass

    def construct(self, dependencies):
        pass

    def set_trending_topics(self, data):
        self._trending_topics = data

    def get_trending_topics(self):
        return self._trending_topics
