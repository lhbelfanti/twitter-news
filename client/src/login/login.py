class Login(object):
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

    def login_user(self):
        raise NotImplementedError('must define login_user to use this base class')
