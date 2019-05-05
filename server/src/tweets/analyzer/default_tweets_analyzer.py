from data import DataManager
from logger import Logger
from utils import regex
from ttp import ttp

from tweets.analyzer import TweetsAnalyzer


class DefaultTweetsAnalyzer(TweetsAnalyzer):
    def __init__(self):
        super().__init__()
        self._data_manager = None
        self._parser = None
        self._trending_topics = None

    def _define_dependencies(self):
        self._add_dependency(DataManager)

    def construct(self, dependencies):
        self._data_manager = self._get_dependency(DataManager, dependencies)
        self._parser = ttp.Parser()
        self._trending_topics = self._data_manager.get_trending_topics()

    def analyze(self):
        Logger.info("Analyzing tweets...")
        for trend in self._trending_topics:
            for tweet in trend.tweets:
                result = self._parser.parse(tweet.text)
                tweet.links = result.urls
                tweet.hashtags = result.tags
                tweet.mentions = result.users
                tweet.cashtags = regex.get_cashtags(tweet.text)
                tweet.text = self._remove(tweet.text, tweet.links, tweet.hashtags, tweet.mentions, tweet.cashtags)

        self._data_manager.set_trending_topics(self._trending_topics)
        Logger.info("----------------------------------------")

    def _remove(self, text, links, hashtags, mentions, cashtags):
        text = self._extract(text, links, '', True)
        text = self._extract(text, hashtags, '#')
        text = self._extract(text, mentions, '@')
        text = self._extract(text, cashtags, '$')
        return text

    def _extract(self, text, array, symbol, link=False):
        for item in array:
            text = text.replace(symbol + item, '' if link else item)
        return text
