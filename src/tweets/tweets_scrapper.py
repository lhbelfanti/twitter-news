import time
import utils
import constants
from trends import TrendFilter
from selenium.webdriver.common.by import By


class TweetsScrapper:
    def __init__(self, driver, trends_data):
        self.driver = driver
        self.trends_data = trends_data
        self.stream_items = None

    def start(self):
        for trend in self.trends_data:
            trend_filter = TrendFilter(self.driver, trend).start()
            self.stream_items = trend_filter.stream_items
            self.get_tweets()

    def get_tweets(self):
        tweets = utils.get_elements_by(By.CLASS_NAME, constants.TWEET_ITEM, self.stream_items)
        for tweet in tweets:
            tweet_data = utils.get_element_by(By.CLASS_NAME, constants.TWEET, tweet)
            tweet_text = utils.get_element_by(By.CLASS_NAME, constants.TWEET_TEXT, tweet_data)
            print(tweet_text.text)

        time.sleep(2)
