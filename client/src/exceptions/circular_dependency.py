from exceptions import Errors


class CircularDependency(Exception):
    def __init__(self, service):
        error = "Circular dependency found while trying to construct {}".format(service)
        super().__init__(error)
        self.errors = Errors.CIRCULAR_DEPENDENCY


