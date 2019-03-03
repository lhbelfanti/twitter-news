import time
import constants
from config import Configuration
from exceptions import LoadingTimeout
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
        self.driver.navigate_to(self.trend.url)
        try:
            self.stream_items = self.driver.wait_until_load(constants.TWEETS_LIST)
            time.sleep(Configuration.config["wait_page_load"])
        except TimeoutException:
            raise LoadingTimeout()

    def add_filters_to_url(self):
        # Adding default filter: ?vertical=default
        self.trend.url += constants.DEFAULT_FILTER
        # Adding location filter: &near=me
        self.trend.url += constants.LOCATION_FILTER
        # Adding language filter: &l=es
        self.trend.url += constants.LANGUAGE_FILTER
