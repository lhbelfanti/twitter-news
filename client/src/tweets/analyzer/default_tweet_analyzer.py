from data import DataManager
from logger import Logger
from utils import regex
from ttp import ttp

from tweets.analyzer import TweetAnalyzer


class DefaultTweetAnalyzer(TweetAnalyzer):
    def __init__(self):
        super().__init__()
        self.data_manager = None
        self.parser = None
        self.trending_topics = None

    def define_dependencies(self):
        self.add_dependency(DataManager)

    def construct(self, dependencies):
        self.data_manager = self.get_dependency(DataManager, dependencies)
        self.parser = ttp.Parser()
        self.trending_topics = self.data_manager.get_trending_topics()

    def analyze(self):
        Logger.info("Analyzing tweets...")
        for trend in self.trending_topics:
            for tweet in trend.tweets:
                result = self.parser.parse(tweet.text)
                tweet.links = result.urls
                tweet.hashtags = result.tags
                tweet.mentions = result.users
                tweet.cashtags = regex.get_cashtags(tweet.text)
                tweet.text = self.remove(tweet.text, tweet.links, tweet.hashtags, tweet.mentions, tweet.cashtags)

        self.data_manager.set_trending_topics(self.trending_topics)
        Logger.info("----------------------------------------")

    def remove(self, text, links, hashtags, mentions, cashtags):
        text = self.extract(text, links, '', True)
        text = self.extract(text, hashtags, '#')
        text = self.extract(text, mentions, '@')
        text = self.extract(text, cashtags, '$')
        return text

    def extract(self, text, array, symbol, link=False):
        for item in array:
            text = text.replace(symbol + item, '' if link else item)
        return text
