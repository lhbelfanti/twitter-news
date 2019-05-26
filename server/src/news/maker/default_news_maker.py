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
        self._config = None
        self._data_manager = None
        self._trends = None
        self._markov_chain = None

    def _define_dependencies(self):
        self._add_dependency(Configuration)
        self._add_dependency(DataManager)

    def construct(self, dependencies):
        self._config = self._get_dependency(Configuration, dependencies)
        self._data_manager = self._get_dependency(DataManager, dependencies)
        self._markov_chain = MarkovChain(self._config)

    def create_news(self):
        trends_processor = TrendsProcessor(self._data_manager.get_trending_topics(), self._config)
        self._trends = trends_processor.get_processed_trends()
        Logger.info("Creating news...")
        self._generate_news()
        Logger.info("----------------------------------------")

    def _generate_news(self):
        for trend in self._trends:
            text = self._markov_chain.execute(trend.texts)
            self._save(trend, text)

    def _save(self, trend, text):
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
