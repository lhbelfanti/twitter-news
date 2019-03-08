class DataManager(object):

    def set_trending_topics(self, data):
        raise NotImplementedError('must define set_trending_topics to use this base class')

    def get_trending_topics(self):
        raise NotImplementedError('must define get_trending_topics to use this base class')

