import json

import unittest
from unittest.mock import MagicMock, patch

from markov_chain import MarkovChain
from news.maker import DefaultNewsMaker


class NewsMakerTest(unittest.TestCase):
    def setUp(self):
        # Dependencies
        attrs = {'get.side_effect': [0, 2, 0, 2]}
        self._config = MagicMock(**attrs)
        # News Maker
        self._news_maker = DefaultNewsMaker()
        self._news_maker._config = self._config
        attrs2 = {'get_trending_topics.return_value': self._get_trends()}
        self._news_maker._data_manager = MagicMock(**attrs2)
        self._news_maker._markov_chain = MarkovChain(self._config)

    def _get_trends(self):
        trends = []
        for i in range(0, 2):
            trend = MagicMock()
            trend.title = "title"
            trend.desc = "desc"
            trend.url = "url"
            trend.tweets_num = "tweets_num"
            trend.users = ["user0", "user1"]
            trend.images = []
            trend.links = ["http://www.test.com"]
            trend.hashtags = ["test"]
            trend.mentions = ["test_man"]
            trend.cashtags = []
            trend.texts = ""

            tweets = []
            for j in range(0, 2):
                tweet = MagicMock()
                tweet.user = "user" + str(j)
                if j == 0:
                    tweet.text = "Muy lejos, más allá de las montañas de palabras, alejados de " \
                                "los países de las vocales y las consonantes, viven los textos simulados. " \
                                "Viven aislados en casas de letras, en la costa de la semántica, un gran " \
                                "océano de lenguas. Un riachuelo llamado Pons fluye por su pueblo y "
                    tweet.links = ["http://www.test1.com"]
                    tweet.hashtags = ["test1"]
                    tweet.mentions = ["test_man1"]
                elif j == 1:
                    tweet.text = "los abastece con las normas necesarias. Hablamos de un país paraisomático " \
                              "en el que a uno le caen pedazos de frases asadas en la boca. #test @test_man " \
                              "http://www.test.com"
                    tweet.links = ["http://www.test2.com"]
                    tweet.hashtags = ["test2"]
                    tweet.mentions = ["test_man2"]
                tweet.images = []
                tweet.cashtags = []
                tweets.append(tweet)
            trend.tweets = tweets

            trends.append(trend)
        return trends

    @patch("logger.Logger.info", return_value="")
    @patch("logger.Logger.error", return_value="")
    @patch("constants.NEWS_JSON", "../../../out/news.json")
    def test_create_news(self, info_mock, error_mock):  # Clean news.json before run this test
        self._news_maker.create_news()
        with open("../../../out/news.json") as json_data:
            news_data = json.load(json_data)

        for i in range(0, len(news_data)):
            trend = news_data[i]
            self.assertEqual(trend["title"], "title")
            self.assertEqual(trend["desc"], "desc")
            self.assertEqual(trend["url"], "urlsrc=tren")
            self.assertEqual(trend["tweets_num"], "tweets_num")
            self.assertIsInstance(trend["text"], str)
            self.assertEqual(trend["images"], [])
            self.assertEqual(sorted((trend["users"])), sorted(["user0", "user1"]))
            self.assertEqual(sorted(trend["links"]), sorted(["http://www.test2.com", "http://www.test1.com"]))
            self.assertEqual(sorted(trend["hashtags"]), sorted(["test2", "test1"]))
            self.assertEqual(sorted(trend["mentions"]), sorted(["test_man1", "test_man2"]))
            self.assertEqual(trend["cashtags"], [])
