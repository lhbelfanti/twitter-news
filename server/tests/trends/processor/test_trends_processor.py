import unittest

from trends.processor import ProcessedTrend
from trends.processor.trends_processor import TrendsProcessor

from unittest.mock import MagicMock, Mock, patch


class TrendsProcessorTest(unittest.TestCase):
    def setUp(self):
        self._trends_mock = []
        for i in range(0, 5):
            self._trends_mock.append(self._create_trend())

    def _create_trend(self):
        trend = MagicMock()
        trend.title = "title"
        trend.desc = "desc"
        trend.url = "url"
        trend.tweets_num = "tweets_num"
        trend.tweets = []
        return trend

    @patch("trends.processor.ProcessedTrend.process", Mock())
    def test_trends_processor_new_instance(self):
        trends_processor = TrendsProcessor(self._trends_mock)
        for trend in trends_processor.processed_trends:
            self.assertIsInstance(trend, ProcessedTrend)

