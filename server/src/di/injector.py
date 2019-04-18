import importlib

from di import Injectable
from exceptions import ServiceNotFound, CircularDependency, NonExistentService, InjectableNotImplemented


class Injector(object):

    def __init__(self, di_config):
        self._di = di_config
        self._services = {}

    def load(self):
        for service in self._di:
            implementation = self._di[service]
            if not hasattr(self._services, service):
                self._services[service] = {}
            self._services[service][implementation] = self._create_instance(implementation)

    def _create_instance(self, service):
        module_name, class_name = service.rsplit(".", 1)
        module = importlib.import_module(module_name)

        if not hasattr(module, class_name):
            raise NonExistentService(class_name, module_name)

        svc = getattr(module, class_name)

        if not issubclass(svc, Injectable):
            raise InjectableNotImplemented(class_name)

        return svc()

    def _internal_get_service(self, service):
        if self._services.get(service, None) is None:
            raise ServiceNotFound(service)

        svc = self._services[service][self._di[service]]

        if not svc.is_constructed():
            self._construct(service, svc)

        return svc

    def _construct(self, service, svc):
        dependencies_map = {}

        deps_checked = [service]
        dependencies = svc.get_dependencies()
        for dependency in dependencies:
            dep_name = dependency.__name__
            deps_checked.append(dep_name)
            self._find_circular_dependency(service, dep_name, deps_checked)
            dependencies_map[dep_name] = self._internal_get_service(dep_name)

        svc.construct(dependencies_map)
        svc.set_constructed()

    def _find_circular_dependency(self, service, dep_name, deps_checked):
        dep_class = self._services[dep_name][self._di[dep_name]]
        dependency_deps = dep_class.get_dependencies()

        deps_size = len(dependency_deps)
        if deps_size > 0:
            for i in range(0, deps_size):
                dep = dependency_deps[i]
                dependency_name = dep.__name__

                if dependency_name in deps_checked:
                    raise CircularDependency(service, dep_class.__class__.__name__, dependency_name)

                deps_checked.append(dependency_name)
                self._find_circular_dependency(service, dependency_name, deps_checked)

    def get_service(self, service_class, by_str=False):
        service_id = service_class.__name__ if not by_str else service_class
        return self._internal_get_service(service_id)
