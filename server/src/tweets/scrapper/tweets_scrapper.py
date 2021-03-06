from di import Injectable


class TweetsScrapper(Injectable):
    def __init__(self):
        super().__init__()

    def get_tweets(self):
        raise NotImplementedError("must define get_tweets to use this base class")

    # Injectable implementations
    def _define_dependencies(self):
        raise NotImplementedError("must define _define_dependencies to use this base class")

    def construct(self, dependencies):
        raise NotImplementedError("must define construct to use this base class")
