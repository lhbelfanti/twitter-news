class TweetsScrapper(object):
    def __init__(self, driver, config, data_manager):
        self.driver = driver
        self.config = config
        self.data_manager = data_manager

    def get_tweets(self, trend):
        raise NotImplementedError('must define get_tweets to use this base class')
