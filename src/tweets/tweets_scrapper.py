import time
import utils
import constants
from exceptions import ElementNotFound
from tweets import Tweet
from trends import TrendFilter
from selenium.webdriver.common.by import By


class TweetsScrapper:
    def __init__(self, driver, trends_data):
        self.driver = driver
        self.trends_data = trends_data
        self.stream_items = None
        self.tweets = []

    def start(self):
        for trend in self.trends_data:
            utils.log("---------- From " + trend.title + ": ----------")
            trend_filter = TrendFilter(self.driver, trend)
            trend_filter.start()
            self.stream_items = trend_filter.stream_items
            self.get_tweets()

    def get_tweets(self):
        tweets_obj = utils.get_elements_by(By.CLASS_NAME, constants.TWEET_ITEM, self.stream_items)
        for tweet_obj in tweets_obj:
            tweet_data = utils.get_element_by(By.CLASS_NAME, constants.TWEET, tweet_obj)
            tweet_user = utils.get_element_by(By.CLASS_NAME, constants.TWEET_USER, tweet_data)
            user = tweet_user.get_attribute(constants.LINK_TAG)
            tweet_text = utils.get_element_by(By.CLASS_NAME, constants.TWEET_TEXT, tweet_data)
            text = tweet_text.text
            images = []
            utils.log("-> " + text)
            try:
                media_container = utils.get_element_by(By.CLASS_NAME, constants.MEDIA_CONTAINER, tweet_data)
                tweet_images = utils.get_elements_by(By.TAG_NAME, constants.IMG_TAG, media_container)
                for img in tweet_images:
                    image = img.get_attribute(constants.SRC_TAG)
                    image = image.replace("'", "")
                    images.append(image)
            except ElementNotFound:
                utils.log("The tweet doesn't contain any image")

            user = user.replace("'", "")
            tweet = Tweet(user, text, images)
            self.tweets.append(tweet)
