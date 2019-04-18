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
        self._driver = None
        self._config = None
        self._data_manager = None
        self._stream_items = None
        self._trends_data = None
        self._trending_topics = []

    def _define_dependencies(self):
        self._add_dependency(Driver)
        self._add_dependency(Configuration)
        self._add_dependency(DataManager)

    def construct(self, dependencies):
        self._driver = self._get_dependency(Driver, dependencies)
        self._config = self._get_dependency(Configuration, dependencies)
        self._data_manager = self._get_dependency(DataManager, dependencies)
        self._trends_data = self._data_manager.get_trending_topics()

    def get_tweets(self):
        Logger.info("Getting tweets...")
        trends_gotten = 0
        trends_to_get = self._config.get("trends_to_get")

        for trend in self._trends_data:
            trends_gotten += 1
            Logger.info("---------- From " + trend.title + ": ----------")
            trend_filter = TrendFilter(self._driver, self._config, trend)
            trend_filter.start()
            self._stream_items = trend_filter.stream_items
            self._driver.scroll_to_bottom(self._config.get("times_to_scroll_to_bottom"))
            self._get_tweets_data(trend)
            if trends_gotten == trends_to_get:
                break

        self._data_manager.set_trending_topics(self._trending_topics)
        Logger.info("----------------------------------------")

    def _get_tweets_data(self, trend):
        tweets_obj = self._driver.get_elements(constants.TWEET_ITEM, self._stream_items)
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
        self._trending_topics.append(trend)
