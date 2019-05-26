from di import Injectable


class Configuration(Injectable):
    def __init__(self):
        super().__init__()

    def define_twitter_ui_version(self, data):
        raise NotImplementedError("must define define_twitter_ui_version to use this base class")

    def get_prop(self, prop, config):
        raise NotImplementedError("must define get_prop to use this base class")

    # Injectable implementations
    def _define_dependencies(self):
        raise NotImplementedError("must define _define_dependencies to use this base class")

    def construct(self, dependencies):
        raise NotImplementedError("must define construct to use this base class")
