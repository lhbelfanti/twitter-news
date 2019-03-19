import json

import constants
from config import Configuration
from data import DataManager
from logger import Logger
from markov_chain import MarkovChain
from news import News
from news.maker import NewsMaker
from trends.processor import TrendsProcessor


class DefaultNewsMaker(NewsMaker):
    def __init__(self):
        super().__init__()
        self.config = None
        self.data_manager = None
        self.trends = None
        self.markov_chain = None

    def define_dependencies(self):
        self.add_dependency(Configuration)
        self.add_dependency(DataManager)

    def construct(self, dependencies):
        self.config = self.get_dependency(Configuration, dependencies)
        self.data_manager = self.get_dependency(DataManager, dependencies)
        self.markov_chain = MarkovChain(self.config)

    def start(self):
        trends_processor = TrendsProcessor(self.data_manager.get_trending_topics())
        self.trends = trends_processor.processed_trends
        Logger.info("Creating news...")
        self.create_news()
        Logger.info("----------------------------------------")

    def create_news(self):
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
