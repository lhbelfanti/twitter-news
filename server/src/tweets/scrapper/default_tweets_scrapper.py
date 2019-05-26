from selenium.webdriver.common.by import By

import hashlib
import constants
from config import Configuration
from data import DataManager
from decorators import version1, version2
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
        trends_to_get = self._config.get_prop("trends_to_get", constants.DE_CFG)

        for trend in self._trends_data:
            obtained_tweets = []
            trends_gotten += 1
            Logger.info("---------- From " + trend.title + ": ----------")
            trend_filter = TrendFilter(self._driver, self._config, trend)
            trend_filter.start()
            stream_items = trend_filter.stream_items
            scroll_to_bottom = self._config.get_prop("times_to_scroll_to_bottom", constants.DE_CFG)
            for i in range(0, scroll_to_bottom):
                # Obtain tweets
                tweets_obj = self._obtain_tweets_obj(stream_items)
                tweets_obj = self._obtain_tweets_obj_v2() if tweets_obj is None else tweets_obj
                for tweet_obj in tweets_obj:
                    tweet = self._get_tweet_data(tweet_obj)
                    if tweet:
                        if not self._was_tweet_added(obtained_tweets, tweet):
                            trend.tweets.append(tweet)

                self._driver.scroll_to_bottom(1)
                self._re_init_trend_filter(trend_filter)
                stream_items = trend_filter.stream_items

            self._trending_topics.append(trend)

            if trends_gotten == trends_to_get:
                break

        self._data_manager.set_trending_topics(self._trending_topics)
        Logger.info("----------------------------------------")

    @version2
    def _re_init_trend_filter(self, trend_filter):
        trend_filter.start(False)

    @version1
    def _obtain_tweets_obj(self, stream_items):
        tweets_obj = self._driver.get_elements(self._config.get_prop("tweet_item"), By.CLASS_NAME, stream_items)
        return tweets_obj

    @version2
    def _obtain_tweets_obj_v2(self):
        tweets_obj = self._driver.get_elements(self._config.get_prop("tweet_item"), By.CLASS_NAME)
        return tweets_obj

    def _was_tweet_added(self, obtained_tweets, tweet):
        tweet_id = tweet.text + tweet.user
        text_hash = hashlib.md5(tweet_id.encode('utf-8')).hexdigest()
        if text_hash not in obtained_tweets:
            obtained_tweets.append(text_hash)
            return False

        return True

    def _get_tweet_data(self, tweet_obj) -> Tweet:
        tweet_data = self._get_tweet_data_element_v1(tweet_obj)
        tweet_data = self._get_tweet_data_element_v2(tweet_obj) if tweet_data is None else tweet_data
        tweet_user = tweet_data.get_element(self._config.get_prop("tweet_user"), By.CSS_SELECTOR)
        user = tweet_user.get_attribute(self._config.get_prop("link_tag"))
        text = ""
        try:
            tweet_text = tweet_data.get_element(self._config.get_prop("tweet_text"), By.CSS_SELECTOR)
            text = tweet_text.text
        except ElementNotFound:
            Logger.info("Tweet without message")

        images = []
        Logger.info(text)
        try:
            media_container = tweet_data.get_element(self._config.get_prop("media_container"), By.CSS_SELECTOR)
            tweet_images = media_container.get_elements(self._config.get_prop("img_tag"))

            for img in tweet_images:
                image = img.get_attribute(self._config.get_prop("src_tag"))
                image = image.replace("'", "")
                images.append(image)
        except ElementNotFound:
            Logger.info("")  # The tweet doesn't contain any image -> empty log because of the spam it causes

        user = user.replace("'", "")
        text = text.replace("\n", '').replace("\r", '').replace("\t", '')
        text = text.strip()

        return Tweet(user, text, images)

    @version1
    def _get_tweet_data_element_v1(self, tweet_obj):
        tweet_data = tweet_obj.get_element(self._config.get_prop("tweet"))
        return tweet_data

    @version2
    def _get_tweet_data_element_v2(self, tweet_obj):
        tweet_data = tweet_obj.get_element(self._config.get_prop("tweet"), By.CSS_SELECTOR)
        return tweet_data
