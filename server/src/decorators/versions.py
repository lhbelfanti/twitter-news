import constants

from di import Injector


def version1(func, return_value=None):
    def wrapper(*args, **kwargs):
        config = Injector.get_instance().get_service("Configuration", True)
        if config.ui_version(constants.V1):
            return func(*args, **kwargs)
        else:
            return return_value

    return wrapper


def version2(func, return_value=None):
    def wrapper(*args, **kwargs):
        config = Injector.get_instance().get_service("Configuration", True)
        if config.ui_version(constants.V2):
            return func(*args, **kwargs)
        else:
            return return_value

    return wrapper
