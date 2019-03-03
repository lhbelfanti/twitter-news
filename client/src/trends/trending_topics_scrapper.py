import constants
import time

from config import Configuration
from exceptions import ElementNotFound, LoadingTimeout
from logger import Logger
from trends import TrendingTopic
from selenium.common.exceptions import TimeoutException


class TrendsScrapper:
    def __init__(self, driver, callback):
        self.driver = driver
        self.trends = []
        self.callback = callback

    def start(self):
        try:
            self.driver.wait_until_load(constants.TRENDS_INNER_MODULE)
            time.sleep(Configuration.config["wait_page_load"])
            self.get_trends_data()
        except TimeoutException:
            raise LoadingTimeout()

    def get_trends_data(self):
        # Get all of the items of the list
        items = self.driver.get_elements(constants.TREND_ITEM)
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
        self.callback(trends_data)
