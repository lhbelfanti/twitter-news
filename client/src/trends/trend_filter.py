import time

from selenium.common.exceptions import TimeoutException

import constants
from exceptions import LoadingTimeout


class TrendFilter:
    def __init__(self, driver, config, trend):
        self.driver = driver
        self.config = config
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
            time.sleep(self.config.get("wait_page_load"))
        except TimeoutException:
            raise LoadingTimeout()

    def add_filters_to_url(self):
        # Adding default filter: ?vertical=default
        self.trend.url += constants.DEFAULT_FILTER
        # Adding location filter: &near=me
        # self.trend.url += constants.LOCATION_FILTER  # Need to handle when there isn't any tweet
        # Adding language filter: &l=es
        self.trend.url += constants.LANGUAGE_FILTER
