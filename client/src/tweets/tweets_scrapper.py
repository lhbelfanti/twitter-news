import time
import constants
from driver import WebDriverUtils as Utils
from config import Configuration
from exceptions import ElementNotFound
from logger import Logger
from tweets import Tweet
from trends import TrendFilter
from selenium.webdriver.common.by import By


class TweetsScrapper:
    def __init__(self, driver, trends_data):
        self.driver = driver
        self.utils = Utils()
        self.trends_data = trends_data
        self.stream_items = None
        self.trending_topics = []

    def start(self):
        trends_to_get = 0
        for trend in self.trends_data:
            trends_to_get += 1
            Logger.info("---------- From " + trend.title + ": ----------")
            trend_filter = TrendFilter(self.driver, trend)
            trend_filter.start()
            self.stream_items = trend_filter.stream_items
            self.scroll_to_bottom(Configuration.config["times_to_scroll_to_bottom"])
            self.get_tweets(trend)
            if trends_to_get == Configuration.config["trends_to_get"]:
                break

    def scroll_to_bottom(self, times):
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for i in range(0, times):
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(Configuration.config["scroll_pause_time"])
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_tweets(self, trend):
        tweets_obj = self.utils.get_elements_by(By.CLASS_NAME, constants.TWEET_ITEM, self.stream_items)
        for tweet_obj in tweets_obj:
            tweet_data = self.utils.get_element_by(By.CLASS_NAME, constants.TWEET, tweet_obj)
            tweet_user = self.utils.get_element_by(By.CLASS_NAME, constants.TWEET_USER, tweet_data)
            user = tweet_user.get_attribute(constants.LINK_TAG)
            tweet_text = self.utils.get_element_by(By.CLASS_NAME, constants.TWEET_TEXT, tweet_data)
            text = tweet_text.text
            images = []
            Logger.info(text)
            try:
                media_container = self.utils.get_element_by(By.CLASS_NAME, constants.MEDIA_CONTAINER, tweet_data)
                tweet_images = self.utils.get_elements_by(By.TAG_NAME, constants.IMG_TAG, media_container)
                for img in tweet_images:
                    image = img.get_attribute(constants.SRC_TAG)
                    image = image.replace("'", "")
                    images.append(image)
            except ElementNotFound:
                Logger.info("")  # The tweet doesn't contain any image -> empty log because of the spam it causes

            user = user.replace("'", "")
            text = text.replace("\n", '').replace("\r", '').replace("\t", '')
            text = text.strip()

            tweet = Tweet(user, text, images)
            trend.tweets.append(tweet)
        self.trending_topics.append(trend)
