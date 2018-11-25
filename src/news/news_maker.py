import json
import constants
from logger import Logger
from trends import TrendsProcessor
from markov_chain import MarkovChain
from news import News


class NewsMaker:
    def __init__(self, trending_topics):
        trends_processor = TrendsProcessor(trending_topics)
        self.trends = trends_processor.processed_trends
        self.markov_chain = MarkovChain()

    def start(self):
        for trend in self.trends:
            text = self.markov_chain.execute(trend.texts)
            self.save(trend, text)

    def save(self, trend, text):
        news = News(trend, text)

        news_data = None
        with open(constants.NEWS_JSON) as json_data:
            try:
                news_data = json.load(json_data)
            except Exception as e:
                Logger.error("Got %s on json.load('news.json')" % e)

        if news_data is None:
            news_data = []

        news_data.append(news.__dict__)
        with open(constants.NEWS_JSON, mode='w', encoding='utf8') as json_file:
            data = json.dumps(news_data, ensure_ascii=False, indent=4)
            json_file.write(data)
