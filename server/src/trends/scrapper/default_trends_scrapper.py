import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import constants
from config import Configuration
from data import DataManager
from decorators import version1, version2
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
            self._driver.wait_until_load(self._config.get_prop("trends_inner_module"))
            time.sleep(self._config.get_prop("wait_page_load", constants.DE_CFG))
            self._obtain_trends()
        except TimeoutException:
            raise LoadingTimeout()

    def _obtain_trends(self):
        self._setup_page()

        # Get all of the items of the list
        items = self._driver.get_elements(self._config.get_prop("trend_item"), By.CSS_SELECTOR)
        quantity = len(items)
        counter = 1
        trends_data = []

        for item in items:
            trend = self.get_trend_data(item)
            if trend is not None:
                trends_data.append(trend)
                Logger.info("Trend " + str(counter) + " of " + str(quantity) + ": " + trend.title)
                counter += 1

        Logger.info("----------------------------------------")
        self._data_manager.set_trending_topics(trends_data)
        Logger.info("----------------------------------------")

    def get_trend_data(self, item) -> TrendingTopic:
        # Get information of each item
        try:
            a_element = self._get_trend_a_tag_v1(item)
            a_element = self._get_trend_a_tag_v2(item) if a_element is None else a_element
            title_element = a_element.get_element(self._config.get_prop("trends_title"), By.CSS_SELECTOR)
            desc_element = a_element.get_element(self._config.get_prop("trends_desc"), By.CSS_SELECTOR, True)
            tweets_element = a_element.get_element(self._config.get_prop("trends_tweets"), By.CSS_SELECTOR)
            link_attr = self._get_link_attr_v1(a_element)
            link_attr = self._get_link_attr_v2(a_element) if link_attr is None else link_attr
            print(link_attr)
        except ElementNotFound:
            # Ignoring Pycharm warning
            # noinspection PyTypeChecker
            return None

        trend = TrendingTopic(title_element.text, desc_element.text, link_attr, tweets_element.text)
        return trend

    @version1
    def _get_link_attr_v1(self, a_element):
        return a_element.get_attribute(self._config.get_prop("link_tag"))

    @version2
    def _get_link_attr_v2(self, a_element):
        a_element.click()
        return self._driver.driver.current_url

    @version1
    def _get_trend_a_tag_v1(self, item):
        return item.get_element(self._config.get_prop("trend_a_tag"), By.CSS_SELECTOR)

    @version2
    def _get_trend_a_tag_v2(self, item):
        return item


    @version2
    def _setup_page(self):
        # Only used in v2.
        first_trend = self._driver.get_element(self._config.get_prop("trend_first_element"), By.CSS_SELECTOR)
        first_trend.click()
        time.sleep(1)
        show_more_btn = self._driver.get_element(self._config.get_prop("trends_show_more_btn"), By.CSS_SELECTOR)
        show_more_btn.click()
