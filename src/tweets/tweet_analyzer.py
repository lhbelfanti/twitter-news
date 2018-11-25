from utils import regex
from ttp import ttp


class TweetAnalyzer:

    def __init__(self, trending_topics):
        self.parser = ttp.Parser()
        self.trending_topics = trending_topics

    def analyze(self):
        for trend in self.trending_topics:
            for tweet in trend.tweets:
                result = self.parser.parse(tweet.text)
                tweet.links = result.urls
                tweet.hashtags = result.tags
                tweet.mentions = result.users
                tweet.cashtags = regex.get_cashtags(tweet.text)
