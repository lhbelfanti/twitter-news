from exceptions import Errors


class InjectableNotImplemented(Exception):
    def __init__(self, srv):
        error = "The service {0} does not implement the Injectable interface".format(srv)
        super().__init__(error)
        self.errors = Errors.INJECTABLE_NOT_IMPLEMENTED
