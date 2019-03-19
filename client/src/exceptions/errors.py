from enum import Enum


class Errors(Enum):
    LOADING_TIMEOUT = 1
    ELEMENT_NOT_FOUND = 2
    SERVICE_NOT_FOUND = 3
    CIRCULAR_DEPENDENCY = 4
