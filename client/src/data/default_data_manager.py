from data import DataManager


class DefaultDataManager(DataManager):

    def __init__(self):
        self.trending_topics = None

    def set_trending_topics(self, data):
        self.trending_topics = data

    def get_trending_topics(self):
        return self.trending_topics
