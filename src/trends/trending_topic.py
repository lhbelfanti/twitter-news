from utils import get_tweets_number


class TrendingTopic:
    def __init__(self, title, desc, url, extra_data):
        self.title = title
        self.desc = desc
        self.url = url
        self.tweets_num = ""
        self.parse_trend_extra_data(extra_data)
        self.tweets = []

    def parse_trend_extra_data(self, tweets_element):
        tweets_data = get_tweets_number(tweets_element)
        if tweets_data["stats"]:
            self.tweets_num = tweets_data["data"]
        else:
            if self.desc == "":
                self.desc = tweets_data["data"]


