class Driver(object):
    def __init__(self, driver, element):
        self.driver = driver
        self.element = element

    def get_element(self, element_id, from_item, by):
        raise NotImplementedError('must define get_element to use this base class')

    def get_elements(self, element_id, from_item, by):
        raise NotImplementedError('must define get_elements to use this base class')

    def wait_until_load(self, element_id, by):
        raise NotImplementedError('must define wait_until_load to use this base class')
