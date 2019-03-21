from trends.processor import ProcessedTrend


class TrendsProcessor:

    def __init__(self, trending_topics):
        self._trending_topics = trending_topics
        self.processed_trends = []
        self._analyze()

    def _analyze(self):
        for trend in self._trending_topics:
            processed_trend = ProcessedTrend(trend)
            processed_trend.process()
            self.processed_trends.append(processed_trend)
