import time
import utils
import constants
from exceptions import LoadingTimeout
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class TrendFilter:
    def __init__(self, driver, trend):
        self.driver = driver
        self.trend = trend
        self.stream_items = None
        self.filter_container = None
        self.select_element = None
        self.current_filter = 0

    def start(self):
        self.add_filters_to_url()

        # Opening trend
        self.driver.get(self.trend.url)
        try:
            self.stream_items = utils.wait_until_load(By.CLASS_NAME, constants.TWEETS_LIST, self.driver)
            time.sleep(constants.WAIT_PAGE_LOAD)
        except TimeoutException:
            raise LoadingTimeout()

    def add_filters_to_url(self):
        # Adding default filter: ?vertical=default
        self.trend.url += constants.DEFAULT_FILTER
        # Adding location filter: &near=me
        self.trend.url += constants.LOCATION_FILTER
        # Adding language filter: &l=es
        self.trend.url += constants.LANGUAGE_FILTER
