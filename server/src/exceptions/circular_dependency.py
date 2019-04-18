from exceptions import Errors


class CircularDependency(Exception):
    def __init__(self, service, dep_class, dependency_name):
        error = "Circular dependency found in {1} -> {2}, while trying to construct {0}."\
            .format(service, dep_class, dependency_name)
        super().__init__(error)
        self.errors = Errors.CIRCULAR_DEPENDENCY


