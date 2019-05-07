from trends.processor import ProcessedTrend


class TrendsProcessor:

    def __init__(self, trending_topics):
        self._trending_topics = trending_topics
        self._processed_trends = []
        self._analyze()

    def _analyze(self):
        for trend in self._trending_topics:
            processed_trend = ProcessedTrend(trend)
            processed_trend.process()
            self._processed_trends.append(processed_trend)

    def get_processed_trends(self):
        return self._processed_trends
