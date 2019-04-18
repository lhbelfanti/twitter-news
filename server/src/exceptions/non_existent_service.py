from exceptions import Errors


class NonExistentService(Exception):
    def __init__(self, srv, pkg):
        error = "Could not found service {0} in package {1}".format(srv, pkg)
        super().__init__(error)
        self.errors = Errors.NON_EXISTENT_SERVICE
