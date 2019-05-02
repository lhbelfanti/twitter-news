from di import Injectable
from trends import TrendingTopic


class TrendsScrapper(Injectable):
    def __init__(self):
        super().__init__()

    def get_trends(self):
        raise NotImplementedError("must define get_trends to use this base class")

    # Should be used to get the data of each trending topic
    def get_trend_data(self, data) -> TrendingTopic:
        raise NotImplementedError("must define get_trend_data to use this base class")

    # Injectable implementations
    def _define_dependencies(self):
        raise NotImplementedError("must define _define_dependencies to use this base class")

    def construct(self, dependencies):
        raise NotImplementedError("must define construct to use this base class")
