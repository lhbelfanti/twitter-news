import unittest

from config import DefaultConfiguration


class ConfigurationTest(unittest.TestCase):
    def setUp(self):
        config_data = {
            "test_value1": 1,
            "test_value2": 10,
            "test_value3": "string1",
            "test_value4": {
                "sub_test_value1": 2,
                "sub_test_value2": 20,
                "sub_test_value3": "string2"
            }
        }
        self._config = DefaultConfiguration()
        self._config.load(config_data)

    def test_should_be_able_to_get_int_value(self):
        self.assertIsInstance(self._config.get_prop("test_value1"), int)

    def test_should_be_able_to_get_string_value(self):
        self.assertIsInstance(self._config.get_prop("test_value3"), str)

    def test_should_be_able_to_get_object_value(self):
        self.assertIsInstance(self._config.get_prop("test_value4"), object)

    def test_should_get_correct_value(self):
        self.assertEqual(self._config.get_prop("test_value1"), 1)
        self.assertEqual(self._config.get_prop("test_value2"), 10)
        self.assertEqual(self._config.get_prop("test_value3"), "string1")

        test_value4_object = {
            "sub_test_value1": 2,
            "sub_test_value2": 20,
            "sub_test_value3": "string2"
        }
        self.assertEqual(self._config.get_prop("test_value4"), test_value4_object)

    def tearDown(self):
        self._config = None
