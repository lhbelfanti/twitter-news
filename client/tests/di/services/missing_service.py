from client.tests.di.services.service import Service


class MissingService(Service):
    def _define_dependencies(self):
        pass

    def construct(self, dependencies):
        pass
