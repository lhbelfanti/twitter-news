from exceptions import Errors


class LoadingTimeout(Exception):
    def __init__(self):
        super().__init__("Loading took too much time")
        self.errors = Errors.ELEMENT_NOT_FOUND
