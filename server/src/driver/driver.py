from di import Injectable


class Driver(Injectable):
    def __init__(self):
        super().__init__()

    def create_driver(self):
        raise NotImplementedError("must define create_driver to use this base class")

    def get_element(self, element_id, from_item, by):
        raise NotImplementedError("must define get_element to use this base class")

    def get_elements(self, element_id, from_item, by):
        raise NotImplementedError("must define get_elements to use this base class")

    def wait_until_load(self, element_id, by):
        raise NotImplementedError("must define wait_until_load to use this base class")
    
    def navigate_to(self, url):
        raise NotImplementedError("must define navigate_to to use this base class")

    def scroll_to_bottom(self, times):
        raise NotImplementedError("must define scroll_to_bottom to use this base class")

    def close(self):
        raise NotImplementedError("must define close to use this base class")

    # Injectable implementations
    def _define_dependencies(self):
        raise NotImplementedError("must define _define_dependencies to use this base class")

    def construct(self, dependencies):
        raise NotImplementedError("must define construct to use this base class")
