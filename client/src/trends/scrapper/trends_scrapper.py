class TrendsScrapper(object):
    def __init__(self, driver, config, data_manager):
        self.driver = driver
        self.config = config
        self.data_manager = data_manager

    def get_trends_data(self):
        raise NotImplementedError('must define get_trends_data to use this base class')
