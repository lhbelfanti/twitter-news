class Tweet:
    def __init__(self, user, text, images):
        self.user = user
        self.text = text
        self.images = images
        self.links = []
        self.hashtags = []
        self.mentions = []
        self.cashtags = []
