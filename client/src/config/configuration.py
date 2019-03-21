from di import Injectable


class Configuration(Injectable):
    def __init__(self):
        super().__init__()

    def get(self, prop):
        raise NotImplementedError("must define get to use this base class")

    # Injectable implementations
    def _define_dependencies(self):
        raise NotImplementedError("must define _define_dependencies to use this base class")

    def construct(self, dependencies):
        raise NotImplementedError("must define construct to use this base class")
