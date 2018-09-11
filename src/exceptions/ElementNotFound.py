from exceptions import Errors


class ElementNotFound(Exception):
    def __init__(self):
        super().__init__("Element not found")
        self.errors = Errors.ELEMENT_NOT_FOUND
