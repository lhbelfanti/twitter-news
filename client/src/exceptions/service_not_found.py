from exceptions import Errors


class ServiceNotFound(Exception):
    def __init__(self, srv):
        error = "Service {} not found. Forgot to inject it or add it to DI.".format(srv)
        super().__init__(error)
        self.errors = Errors.SERVICE_NOT_FOUND
