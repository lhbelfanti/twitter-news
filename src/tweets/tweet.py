class Tweet:
    def __init__(self, user, text, images, links=None, hashtags=None, mentions=None, cashtags=None):
        self.user = user
        self.text = text
        self.images = images
        self.links = self.check_value(links)
        self.hashtags = self.check_value(hashtags)
        self.mentions = self.check_value(mentions)
        self.cashtags = self.check_value(cashtags)

    def check_value(self, data):
        if data is None:
            return []
        else:
            return data
