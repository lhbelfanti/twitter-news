from di import Injectable


class Driver(Injectable):
    def __init__(self):
        super().__init__()

    def get_element(self, element_id, from_item, by):
        raise NotImplementedError('must define get_element to use this base class')

    def get_elements(self, element_id, from_item, by):
        raise NotImplementedError('must define get_elements to use this base class')

    def wait_until_load(self, element_id, by):
        raise NotImplementedError('must define wait_until_load to use this base class')

    def define_dependencies(self):
        raise NotImplementedError('must define define_dependencies to use this base class')

    def construct(self, dependencies):
        raise NotImplementedError('must define construct to use this base class')
