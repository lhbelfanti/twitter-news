import unittest

from ttp import ttp

from unittest.mock import MagicMock, Mock, patch

from tweets.analyzer import DefaultTweetsAnalyzer


class TweetsAnalyzerTest(unittest.TestCase):
    def setUp(self):
        self._tweets_analyzer = DefaultTweetsAnalyzer()
        self._tweets_analyzer._trending_topics = self._create_trends()
        self._tweets_analyzer._parser = ttp.Parser()
        self._tweets_analyzer._data_manager = Mock()

    def _create_trends(self):
        trends = []
        for i in range(0, 5):
            trend = MagicMock()
            trend.title = "title"
            trend.desc = "desc"
            trend.url = "url"
            trend.tweets_num = "tweets_num"
            trend.tweets = self._create_tweets()
            trends.append(trend)
        return trends

    def _create_tweets(self):
        tweets = []
        for i in range(0, 5):
            tweet = MagicMock()
            tweet.user = "user"
            tweet.text = "This is a text that contains #hashtag1 #hashtag2#hashtag3 " \
                         "and also contains http://www.test1.com https://test2.com " \
                         "www.test3.net www.test4 test5.com.ar test6.ar" \
                         "and also contains @mention1  @mention2@mention3" \
                         "and also contains $CTA $CTB$CTC"
            tweet.images = []
            tweet.links = []
            tweet.hashtags = []
            tweet.mentions = []
            tweet.cashtags = []
            tweets.append(tweet)
        return tweets

    @patch("logger.Logger.info", return_value="")
    def test_get_tweets(self, logger_mock):
        self._tweets_analyzer.analyze()
        text = "This is a text that contains hashtag1 hashtag2#hashtag3 and also contains    " \
               "www.test4 test5.com.ar test6.arand also contains mention1  mention2@mention3and " \
               "also contains $CTA $CTB$CTC"
        hashtags = ["hashtag1", "hashtag2"]
        links = ["http://www.test1.com", "https://test2.com", "www.test3.net"]
        mentions = ["mention1", "mention2"]
        cashtags = ["$CTA", "$CTB", "$CTC"]
        for trend in self._tweets_analyzer._trending_topics:
            for tweet in trend.tweets:
                self.assertEqual(tweet.text, text)
                self.assertEqual(tweet.hashtags, hashtags)
                self.assertEqual(tweet.links, links)
                self.assertEqual(tweet.mentions, mentions)
                self.assertEqual(tweet.cashtags, cashtags)

    def tearDown(self):
        self._tweets_analyzer = None
