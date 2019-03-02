import abc


class DriverUtils(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_element_by(self, by, element_id, from_item):
        raise NotImplementedError('users must define get_element_by to use this base class')

    @abc.abstractmethod
    def get_elements_by(self, by, element_id, from_item):
        raise NotImplementedError('users must define get_elements_by to use this base class')

    @abc.abstractmethod
    def wait_until_load(self, by, element_id, driver):
        raise NotImplementedError('users must define wait_until_load to use this base class')