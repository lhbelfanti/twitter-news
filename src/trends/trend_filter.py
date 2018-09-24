import time
import utils
import constants
from exceptions import LoadingTimeout
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException


class TrendFilter:
    def __init__(self, driver, trend):
        self.driver = driver
        self.trend = trend
        self.stream_items = None
        self.filter_container = None
        self.current_select_element = None

    def start(self):
        self.open_trend(self.trend.url)
        self.click_show_filter()
        self.process_filters()

    def open_trend(self, url):
        self.driver.get(url)
        try:
            self.stream_items = utils.wait_until_load(By.CLASS_NAME, constants.TWEETS_LIST, self.driver)
            time.sleep(2)
        except TimeoutException:
            raise LoadingTimeout()

    def click_show_filter(self):
        self.filter_container = utils.get_element_by(By.CLASS_NAME, constants.FILTER_CONTAINER, self.driver)
        filter_button = utils.get_element_by(By.CLASS_NAME, constants.FILTER_BUTTON, self.filter_container)
        filter_button.click()

    def process_filters(self):
        filters = utils.get_elements_by(By.CLASS_NAME, constants.FILTERS, self.filter_container)
        for filter_item in filters:
            # Get filter type
            filter_type = filter_item.get_attribute(constants.FILTER_ATTRIBUTE)
            # Get 'select' element
            self.current_select_element = Select(
                utils.get_element_by(By.CLASS_NAME, constants.FILTER_SELECT, filter_item))
            # Choose 'select' option by filter type
            self.select_filter(filter_type)

    def select_filter(self, filter_type):
        if filter_type == constants.FILTER_BY_SOCIAL:
            pass
        elif filter_type == constants.FILTER_BY_LOCATION:
            pass
        elif filter_type == constants.FILTER_BY_LANGUAGE:
            pass
        elif filter_type == constants.FILTER_BY_QUALITY:
            pass
