class NewsMaker(object):
    def __init__(self, config, data_manager):
        self.config = config
        self.data_manager = data_manager

    def create_news(self):
        raise NotImplementedError('must define create_news to use this base class')
