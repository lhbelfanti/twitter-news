import unittest

from server.tests.di.services import Service, Service0, MissingService
from server.tests.di.services.circular_dependency import Service1, Service3, Service7
from di import Injector
from exceptions import ServiceNotFound, CircularDependency, NonExistentService, InjectableNotImplemented


class InjectorTest(unittest.TestCase):
    def setUp(self):
        self._di_config = {
            "Service": "server.tests.di.services.Service0",
            "Service0": "server.tests.di.services.Service0",
            "Service1": "server.tests.di.services.circular_dependency.Service1",
            "Service2": "server.tests.di.services.circular_dependency.Service2",
            "Service3": "server.tests.di.services.circular_dependency.Service3",
            "Service4": "server.tests.di.services.circular_dependency.Service4",
            "Service5": "server.tests.di.services.circular_dependency.Service5",
            "Service6": "server.tests.di.services.circular_dependency.Service6",
            "Service7": "server.tests.di.services.circular_dependency.Service7"
        }
        self._injector = None
        self._create_injector()

    def _create_injector(self):
        self._injector = Injector(self._di_config)
        self._injector.load()

    def test_should_get_service(self):
        # By class and by string
        self.assertIsInstance(self._injector.get_service(Service), Service0)
        self.assertIsInstance(self._injector.get_service("Service", True), Service0)

    def test_should_throw_missing_service(self):
        with self.assertRaises(ServiceNotFound) as cm:
            self._injector.get_service(MissingService)
        print(cm.exception.args[0])

    def test_should_return_same_service(self):
        self.assertEqual(self._injector.get_service(Service), self._injector.get_service(Service))

    def test_should_detect_simple_circular_dependency(self):
        with self.assertRaises(CircularDependency) as cm:
            self._injector.get_service(Service1)
        print(cm.exception.args[0])

    def test_should_detect_complex_circular_dependency(self):
        with self.assertRaises(CircularDependency) as cm:
            self._injector.get_service(Service3)
        print(cm.exception.args[0])
        # Graph example:
        # Service3 -> Service4 -> Service5
        #          -> Service5 -> Service4 -> Service5 // Circular dependency
        #                      -> Service6 -> Service3 // Circular dependency

    def test_circular_dependency_false_positive_bug(self):
        with self.assertRaises(CircularDependency) as cm:
            self._injector.get_service(Service7)
        print(cm.exception.args[0])

    def test_non_existent_service(self):
        self._di_config = {"NonExistentService": "server.tests.di.services.NonExistentService"}

        with self.assertRaises(NonExistentService) as cm:
            self._create_injector()
        print(cm.exception.args[0])

    def test_injectable_not_implemented(self):
        self._di_config = {"InjectableNotImplemented": "server.tests.di.services.InjectableNotImplemented"}

        with self.assertRaises(InjectableNotImplemented) as cm:
            self._create_injector()
        print(cm.exception.args[0])

    def tearDown(self):
        self._di_config = None
        self._injector = None
