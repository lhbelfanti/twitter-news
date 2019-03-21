import importlib

from exceptions import ServiceNotFound, CircularDependency


class Injector(object):

    def __init__(self, di_config):
        self._di = di_config
        self._services = {}
        self._load()

    def _load(self):
        for service in self._di:
            implementation = self._di[service]
            if not hasattr(self._services, service):
                self._services[service] = {}
            self._services[service][implementation] = self._create_instance(implementation)

    def _create_instance(self, service):
        module_name, class_name = service.rsplit(".", 1)
        svc = getattr(importlib.import_module(module_name), class_name)
        return svc()

    def _internal_get_service(self, service):
        svc = self._services[service][self._di[service]]

        if not svc:
            raise ServiceNotFound(svc)

        if not svc.is_constructed():
            self._construct(service, svc)

        return svc

    def _construct(self, service, svc):
        dependencies_map = {}

        dependencies = svc.get_dependencies()
        for dependency in dependencies:
            dep_name = dependency.__name__
            dep_class = self._services[dep_name][self._di[dep_name]]
            dependency_deps = dep_class.get_dependencies()

            dependency_deps_size = len(dependency_deps)
            if dependency_deps_size > 0:
                dependency_deps_end = dependency_deps[-1]
                for i in range(0, dependency_deps_size):
                    dep = dependency_deps[i]
                    if dep == service:
                        if dep != dependency_deps_end:
                            raise CircularDependency(service.__name__)

            dependencies_map[dep_name] = self._internal_get_service(dep_name)

        svc.construct(dependencies_map)
        svc.set_constructed()

    def get_service(self, service_class):
        return self._internal_get_service(service_class.__name__)