import unittest

from unittest.mock import MagicMock, Mock, patch

from data import DefaultDataManager
from driver import TwitterDriver
from tweets.scrapper import DefaultTweetsScrapper


class TweetsScrapperTest(unittest.TestCase):

    methods_calls = {}

    def setUp(self):
        # Dependencies
        self._driver = TwitterDriver()
        attrs = {'get.return_value': 5}
        self._config = MagicMock(**attrs)
        self._driver.config = self._config
        self._driver.create_driver()
        self._data_manager = DefaultDataManager()
        # Tweets Scrapper
        self._tweets_scrapper = DefaultTweetsScrapper()
        self._tweets_scrapper._driver = self._driver
        self._tweets_scrapper._config = self._config
        self._tweets_scrapper._data_manager = self._data_manager
        self._tweets_scrapper._trends_data = self._create_trends()

        self._reset_methods_calls()

    def _reset_methods_calls(self):
        # Methods calls
        TweetsScrapperTest.methods_calls = {
            "_create_tweets": {"calls": 0, "data": []},
            "_create_new_tweet": {"calls": 0, "data": []}
        }

    def _create_trends(self):
        trends = []
        for i in range(0, 5):
            trend = MagicMock()
            trend.title = "title"
            trend.desc = "desc"
            trend.url = "url"
            trend.tweets_num = "tweets_num"
            trend.tweets = []
            trends.append(trend)
        return trends

    def _create_tweets(self, element_id, from_item):
        tweets = []
        for i in range(0, 5):
            tweet = MagicMock()
            tweet.user = "user"
            tweet.text = "text"
            tweet.images = []
            tweet.links = []
            tweet.hashtags = []
            tweet.mentions = []
            tweet.cashtags = []
            tweets.append(tweet)
        TweetsScrapperTest.methods_calls["_create_tweets"]["calls"] += 1
        return tweets

    def _create_new_tweet(self, tweet_obj):
        tweet = MagicMock()
        tweet.user = "user"
        tweet.text = "text"
        tweet.images = []
        tweet.links = []
        tweet.hashtags = []
        tweet.mentions = []
        tweet.cashtags = []
        TweetsScrapperTest.methods_calls["_create_new_tweet"]["calls"] += 1
        TweetsScrapperTest.methods_calls["_create_new_tweet"]["data"].append(tweet)
        return tweet

    @patch("logger.Logger.info", return_value="")
    @patch("driver.TwitterDriver.scroll_to_bottom", Mock())
    @patch("driver.TwitterDriver.get_elements", new=_create_tweets)
    @patch("trends.TrendFilter.start", Mock())
    @patch("tweets.scrapper.DefaultTweetsScrapper._get_tweet_data", new=_create_new_tweet)
    def test_get_tweets(self, logger_mock):
        self._reset_methods_calls()
        self._tweets_scrapper.get_tweets()
        self.assertEqual(TweetsScrapperTest.methods_calls["_create_tweets"]["calls"], 5)  # called once per trend
        self.assertEqual(TweetsScrapperTest.methods_calls["_create_new_tweet"]["calls"], 25)  # 5 tweets per trend
        data_manager_trends = self._tweets_scrapper._data_manager.get_trending_topics()
        tweets = TweetsScrapperTest.methods_calls["_create_new_tweet"]["data"]
        counter = 0
        for i in range(0, len(self._tweets_scrapper._trends_data)):
            trend = data_manager_trends[i]
            trend_tweets = trend.tweets
            for j in range(0, len(data_manager_trends)):
                self.assertEqual(trend_tweets[j], tweets[counter])
                counter += 1

    def tearDown(self):
        self._driver.close()
        self._config = None
        self._data_manager = None
        self._tweets_scrapper = None
