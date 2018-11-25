import constants
from utils import add_dot_at_the_end


class ProcessedTrend:
    def __init__(self, trend):
        self.title = trend.title
        self.desc = trend.desc
        self.url = trend.url.split(constants.TREND_URL_TAG)[0] + constants.TREND_URL_TAG
        self.tweets_num = trend.tweets_num
        self.tweets = trend.tweets
        # Variables with processed data
        self.users = []
        self.texts = ""
        self.images = []
        self.links = []
        self.hashtags = []
        self.mentions = []
        self.cashtags = []

    def process(self):
        for tweet in self.tweets:
            self.users.append(tweet.user)
            self.texts += add_dot_at_the_end(tweet.text)
            self.images.extend(tweet.images)
            self.links.extend(tweet.links)
            self.hashtags.extend(tweet.hashtags)
            self.mentions.extend(tweet.mentions)
            self.cashtags.extend(tweet.cashtags)

        self.clean()

    def clean(self):
        self.users = list(set(self.users))
        self.images = list(set(self.images))
        self.links = list(set(self.links))
        self.hashtags = list(set(self.hashtags))
        self.mentions = list(set(self.mentions))
        self.cashtags = list(set(self.cashtags))
