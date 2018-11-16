import json
import constants
from trends import TrendingTopic
from trends import ProcessedTrend
from tweets import Tweet


class TrendsProcessor:

    def __init__(self):
        self.processed_trends = []
        self.open_file()

    def open_file(self):
        with open(constants.TRENDS_JSON) as json_data:
            data = json.load(json_data)

        self.analyze(data)

    def analyze(self, data):
        for t in data:
            trend = self.create_trending_topic(t)
            for tw in t.get("tweets", []):
                tweet = self.create_tweet(tw)
                trend.tweets.append(tweet)

            processed_trend = ProcessedTrend(trend)
            processed_trend.process()
            self.processed_trends.append(processed_trend)
            processed_trend.clean()

    def create_trending_topic(self, t):
        trend = TrendingTopic(t.get("title", ""), t.get("desc", ""), t.get("url", ""))
        trend.tweets_num = t.get("tweets_num", "")
        return trend

    def create_tweet(self, tw):
        tweet = Tweet(tw.get("user", ""), tw.get("text", ""), tw.get("images", []), tw.get("links", []),
                      tw.get("hashtags", []), tw.get("mentions", []), tw.get("chashtags", []))
        return tweet
