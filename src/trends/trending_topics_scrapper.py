import constants
import utils
import time
from exceptions import ElementNotFound, LoadingTimeout
from trends import TrendingTopic
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class TrendsScrapper:
    def __init__(self, driver, callback):
        self.driver = driver
        self.trends = []
        self.callback = callback

    def start(self):
        try:
            utils.wait_until_load(By.CLASS_NAME, constants.TRENDS_INNER_MODULE, self.driver)
            self.get_trends_data()
        except TimeoutException:
            raise LoadingTimeout()

    def get_trends_data(self):
        time.sleep(2)

        # Get all of the items of the list
        items = utils.get_elements_by(By.CLASS_NAME, constants.TREND_ITEM, self.driver)
        quantity = len(items)
        counter = 1
        trends_data = []
        for item in items:
            # Get information of each item
            try:
                a_element = utils.get_element_by(By.CLASS_NAME, constants.TREND_A_TAG, item)
                title_element = utils.get_element_by(By.CLASS_NAME, constants.TRENDS_TITLE, a_element)
                desc_element = utils.get_element_by(By.CLASS_NAME, constants.TRENDS_DESC, a_element)
                tweets_element = utils.get_element_by(By.CLASS_NAME, constants.TRENDS_TWEETS, a_element)
                link_attr = a_element.get_attribute(constants.LINK_TAG)
            except ElementNotFound:
                continue

            title = title_element.text
            trend = TrendingTopic(title, desc_element.text, link_attr, tweets_element.text)
            trends_data.append(trend)

            utils.log("Trend " + str(counter) + " of " + str(quantity) + ": " + title)
            counter += 1

        self.callback(trends_data)

