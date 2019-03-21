import time

from selenium.common.exceptions import TimeoutException

import constants
from exceptions import LoadingTimeout


class TrendFilter:
    def __init__(self, driver, config, trend):
        self._driver = driver
        self._config = config
        self._trend = trend
        self.stream_items = None

    def start(self):
        self._add_filters_to_url()

        # Opening trend
        self._driver.navigate_to(self._trend.url)
        try:
            self.stream_items = self._driver.wait_until_load(constants.TWEETS_LIST)
            time.sleep(self._config.get("wait_page_load"))
        except TimeoutException:
            raise LoadingTimeout()

    def _add_filters_to_url(self):
        # Adding default filter: ?vertical=default
        self._trend.url += constants.DEFAULT_FILTER
        # Adding location filter: &near=me
        # self.trend.url += constants.LOCATION_FILTER  # Need to handle when there isn't any tweet
        # Adding language filter: &l=es
        self._trend.url += constants.LANGUAGE_FILTER
