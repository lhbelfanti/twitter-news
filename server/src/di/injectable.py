class Injectable(object):

    def __init__(self):
        self._dependencies = []
        self._constructed = False
        self._define_dependencies()

    def _define_dependencies(self):
        raise NotImplementedError("must define _define_dependencies to use this base class")

    def construct(self, dependencies):
        raise NotImplementedError("must define construct to use this base class")

    def get_dependencies(self):
        return self._dependencies

    def set_constructed(self):
        self._constructed = True

    def is_constructed(self):
        return self._constructed

    def _add_dependency(self, dependency):
        self._dependencies.append(dependency)

    def _get_dependency(self, class_object, dependencies):
        return dependencies[class_object.__name__]
