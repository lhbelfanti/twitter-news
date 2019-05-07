import unittest

from unittest.mock import MagicMock, Mock, patch

from data import DefaultDataManager
from driver import TwitterDriver
from exceptions import LoadingTimeout
from trends import TrendingTopic
from trends.scrapper import DefaultTrendsScrapper


class TrendsScrapperTest(unittest.TestCase):

    methods_calls = {}

    def setUp(self):
        # Dependencies
        self._driver = TwitterDriver()
        attrs = {'get.return_value': 0}
        self._config = MagicMock(**attrs)
        self._driver.config = self._config
        self._driver.create_driver()
        self._data_manager = DefaultDataManager()
        # Trends Scrapper
        self._trends_scrapper = DefaultTrendsScrapper()
        self._trends_scrapper._driver = self._driver
        self._trends_scrapper._config = self._config
        self._trends_scrapper._data_manager = self._data_manager

        self._reset_methods_calls()

    def _reset_methods_calls(self):
        # Methods calls
        TrendsScrapperTest.methods_calls = {
            "_get_elements_mock": {"calls": 0, "data": []},
            "_get_trend_data_mock": {"calls": 0, "data": []},
            "_get_element": {"calls": 0, "data": None}
        }

    def _get_elements_mock(self, element_id):
        elements = []
        for i in range(0, 8):
            web_element_mock = MagicMock()
            web_element_mock.desc = "desc mock"
            web_element_mock.title = "title mock"
            web_element_mock.tweets = ["test", "test"]
            web_element_mock.tweets_num = "desc mock"
            web_element_mock.url = "url mock"
            elements.append(web_element_mock)
        TrendsScrapperTest.methods_calls["_get_elements_mock"]["calls"] += 1
        return elements

    def _get_trend_data_mock(self, item):
        trend_mock = MagicMock()
        trend_mock.desc = item.desc
        trend_mock.title = item.title
        trend_mock.tweets = item.tweets
        trend_mock.tweets_num = item.tweets_num
        trend_mock.url = item.url
        TrendsScrapperTest.methods_calls["_get_trend_data_mock"]["calls"] += 1
        TrendsScrapperTest.methods_calls["_get_trend_data_mock"]["data"].append(trend_mock)
        return trend_mock

    @patch("logger.Logger.info", return_value="")
    @patch("driver.TwitterDriver.wait_until_load", Mock())
    @patch("driver.TwitterDriver.get_elements", new=_get_elements_mock)
    @patch("trends.scrapper.DefaultTrendsScrapper.get_trend_data", new=_get_trend_data_mock)
    def test_get_trends(self, logger_mock):
        self._reset_methods_calls()
        self._trends_scrapper.get_trends()
        self.assertEqual(TrendsScrapperTest.methods_calls["_get_elements_mock"]["calls"], 1)
        self.assertEqual(TrendsScrapperTest.methods_calls["_get_trend_data_mock"]["calls"], 8)
        data_manager_trends = self._trends_scrapper._data_manager.get_trending_topics()
        trending_topics = TrendsScrapperTest.methods_calls["_get_trend_data_mock"]["data"]
        for i in range(0, len(data_manager_trends)):
            self.assertEqual(data_manager_trends[i], trending_topics[i])

    def _create_item_mock(self):
        item_mock = MagicMock()
        item_mock.desc = "desc mock"
        item_mock.title = "title mock"
        item_mock.tweets = ["test", "test"]
        item_mock.tweets_num = "desc mock"
        item_mock.url = "url mock"
        item_mock.text = None
        return item_mock

    def _get_element(self):
        item_mock = self._create_item_mock()
        item_mock.get_element.return_value = self._create_item_mock()
        return item_mock

    def test_get_trend_data(self):
        self._reset_methods_calls()
        attrs = {'get_element.return_value': self._get_element()}
        item = MagicMock(**attrs)
        trend = self._trends_scrapper.get_trend_data(item)
        self.assertIsInstance(trend, TrendingTopic)

    @patch("logger.Logger.info", return_value="")
    def test_should_throw_timeout_exception(self, logger_mock):
        self._reset_methods_calls()
        with self.assertRaises(LoadingTimeout) as cm:
            self._trends_scrapper.get_trends()
        print(cm.exception.args[0])

    def tearDown(self):
        self._driver.close()
        self._config = None
        self._data_manager = None
        self._trends_scrapper = None
