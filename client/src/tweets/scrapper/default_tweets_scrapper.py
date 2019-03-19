import constants
from config import Configuration
from data import DataManager
from driver import Driver
from exceptions import ElementNotFound
from logger import Logger
from trends import TrendFilter
from tweets import Tweet
from tweets.scrapper import TweetsScrapper


class DefaultTweetsScrapper(TweetsScrapper):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.config = None
        self.data_manager = None
        self.stream_items = None
        self.trends_data = None
        self.trending_topics = []

    def define_dependencies(self):
        self.add_dependency(Driver)
        self.add_dependency(Configuration)
        self.add_dependency(DataManager)

    def construct(self, dependencies):
        self.driver = self.get_dependency(Driver, dependencies)
        self.config = self.get_dependency(Configuration, dependencies)
        self.data_manager = self.get_dependency(DataManager, dependencies)
        self.trends_data = self.data_manager.get_trending_topics()

    def start(self):
        Logger.info("Getting tweets...")
        trends_gotten = 0
        trends_to_get = self.config.get("trends_to_get")

        for trend in self.trends_data:
            trends_gotten += 1
            Logger.info("---------- From " + trend.title + ": ----------")
            trend_filter = TrendFilter(self.driver, self.config, trend)
            trend_filter.start()
            self.stream_items = trend_filter.stream_items
            self.driver.scroll_to_bottom(self.config.get("times_to_scroll_to_bottom"))
            self.get_tweets(trend)
            if trends_gotten == trends_to_get:
                break

        self.data_manager.set_trending_topics(self.trending_topics)
        Logger.info("----------------------------------------")

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
