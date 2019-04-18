import datetime


class News:
    def __init__(self, trend, text):
        now = datetime.datetime.now()
        self.title = trend.title
        self.desc = trend.desc
        self.url = trend.url
        self.tweets_num = trend.tweets_num
        self.creation_date = now.strftime("%Y-%m-%d %H:%M")
        self.title = trend.title
        self.text = text
        self.images = trend.images
        self.users = trend.users
        self.links = trend.links
        self.hashtags = trend.hashtags
        self.mentions = trend.mentions
        self.cashtags = trend.cashtags