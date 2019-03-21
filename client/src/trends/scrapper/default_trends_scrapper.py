import time

from selenium.common.exceptions import TimeoutException

import constants
from config import Configuration
from data import DataManager
from driver import Driver
from exceptions import ElementNotFound, LoadingTimeout
from logger import Logger
from trends import TrendingTopic
from trends.scrapper import TrendsScrapper


class DefaultTrendsScrapper(TrendsScrapper):
    def __init__(self):
        super().__init__()
        self._trends = []
        self._driver = None
        self._config = None
        self._data_manager = None

    def _define_dependencies(self):
        self._add_dependency(Driver)
        self._add_dependency(Configuration)
        self._add_dependency(DataManager)

    def construct(self, dependencies):
        self._driver = self._get_dependency(Driver, dependencies)
        self._config = self._get_dependency(Configuration, dependencies)
        self._data_manager = self._get_dependency(DataManager, dependencies)

    def get_trends(self):
        Logger.info("Getting trends...")
        try:
            self._driver.wait_until_load(constants.TRENDS_INNER_MODULE)
            time.sleep(self._config.get("wait_page_load"))
            self._get_trends_data()
        except TimeoutException:
            raise LoadingTimeout()

    def _get_trends_data(self):
        # Get all of the items of the list
        items = self._driver.get_elements(constants.TREND_ITEM)
        quantity = len(items)
        counter = 1
        trends_data = []

        for item in items:
            # Get information of each item
            try:
                a_element = item.get_element(constants.TREND_A_TAG)
                title_element = a_element.get_element(constants.TRENDS_TITLE)
                desc_element = a_element.get_element(constants.TRENDS_DESC)
                tweets_element = a_element.get_element(constants.TRENDS_TWEETS)
                link_attr = a_element.get_attribute(constants.LINK_TAG)
            except ElementNotFound:
                continue

            title = title_element.text
            trend = TrendingTopic(title, desc_element.text, link_attr, tweets_element.text)
            trends_data.append(trend)

            Logger.info("Trend " + str(counter) + " of " + str(quantity) + ": " + title)
            counter += 1

        Logger.info("----------------------------------------")
        self._data_manager.set_trending_topics(trends_data)

        Logger.info("----------------------------------------")
