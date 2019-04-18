from server.tests.di.services.service import Service


# Simple circular dependency case
class Service1(Service):
    def _define_dependencies(self):
        self._add_dependency(Service2)

    def construct(self, dependencies):
        pass


class Service2(Service):
    def _define_dependencies(self):
        self._add_dependency(Service1)

    def construct(self, dependencies):
        pass


# Complex circular dependency case
class Service3(Service):
    def _define_dependencies(self):
        self._add_dependency(Service4)
        self._add_dependency(Service5)

    def construct(self, dependencies):
        pass


class Service4(Service):
    def _define_dependencies(self):
        self._add_dependency(Service5)

    def construct(self, dependencies):
        pass


class Service5(Service):
    def _define_dependencies(self):
        self._add_dependency(Service4)
        self._add_dependency(Service6)

    def construct(self, dependencies):
        pass


class Service6(Service):
    def _define_dependencies(self):
        self._add_dependency(Service3)

    def construct(self, dependencies):
        pass


# False positive case
class Service7(Service):
    def _define_dependencies(self):
        self._add_dependency(Service7)

    def construct(self, dependencies):
        pass

