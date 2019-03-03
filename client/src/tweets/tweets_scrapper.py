import constants
from config import Configuration
from exceptions import ElementNotFound
from logger import Logger
from tweets import Tweet
from trends import TrendFilter


class TweetsScrapper:
    def __init__(self, driver, trends_data):
        self.driver = driver
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
            self.driver.scroll_to_bottom(Configuration.config["times_to_scroll_to_bottom"])
            self.get_tweets(trend)
            if trends_to_get == Configuration.config["trends_to_get"]:
                break

    def get_tweets(self, trend):
        tweets_obj = self.driver.get_elements(constants.TWEET_ITEM, self.stream_items)
        for tweet_obj in tweets_obj:
            tweet_data = tweet_obj.get_element(constants.TWEET)
            tweet_user = tweet_data.get_element(constants.TWEET_USER)
            user = tweet_user.get_attribute(constants.LINK_TAG)
            tweet_text = tweet_data.get_element(constants.TWEET_TEXT)
            text = tweet_text.text
            images = []
            Logger.info(text)
            try:
                media_container = tweet_data.get_element(constants.MEDIA_CONTAINER)
                tweet_images = media_container.get_elements(constants.IMG_TAG)

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
