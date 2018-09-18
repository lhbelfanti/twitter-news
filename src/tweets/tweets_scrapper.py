import time
import utils
import constants
from exceptions import LoadingTimeout
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class TweetsScrapper:
    def __init__(self, driver, trends_data):
        self.driver = driver
        self.trends_data = trends_data

    def start(self):
        for trend in self.trends_data:
            self.get_tweets(trend)

    def get_tweets(self, trend):
        self.open_trend(trend.url)
        time.sleep(2)
        pass

    def open_trend(self, url):
        self.driver.get(url)
        try:
            element = utils.wait_until_load(By.CLASS_NAME, constants.TRENDS_INNER_MODULE, self.driver)
        except TimeoutException:
            raise LoadingTimeout()