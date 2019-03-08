class TweetAnalyzer(object):
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def analyze(self):
        raise NotImplementedError('must define analyze to use this base class')
