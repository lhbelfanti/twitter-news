import re
import constants
from exceptions import ElementNotFound
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec


def get_element_by(by, element_id, from_item):
    elements = from_item.find_elements(by, element_id)
    size = len(elements)

    if size > 0:
        return elements[0]
    else:
        raise ElementNotFound()


def get_elements_by(by, element_id, from_item):
    elements = from_item.find_elements(by, element_id)
    return elements


def wait_until_load(by, element_id, driver):
    return WebDriverWait(driver, constants.LOADING_TIMEOUT).until(
        Ec.element_to_be_clickable((by, element_id)))


def get_tweets_number(msg):
    splitted = msg.split(' ')
    pattern = re.compile("(\d*[,.]\d*)[a-zA-Z]*")

    return_data = {"stats": False, "data": msg}
    if pattern.match(splitted[0]):
        return_data["stats"] = True
        return_data["data"] = splitted[0]

    return return_data
