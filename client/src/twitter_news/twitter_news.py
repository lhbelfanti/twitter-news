import os
from subprocess import call

import constants
from data import DefaultDataManager
from logger import Logger
from login import DefaultLogin
from news.maker import DefaultNewsMaker
from trends.scrapper import DefaultTrendsScrapper
from tweets.analyzer import DefaultTweetAnalyzer
from tweets.scrapper import DefaultTweetsScrapper


class TwitterNews:
    def __init__(self, driver, config):
        Logger.info("Opening Twitter...")
        self.driver = driver
        title = self.driver.navigate_to(constants.TWITTER_URL)
        Logger.info(title)
        Logger.info("----------------------------------------")
        self.data_manager = DefaultDataManager()
        self.config = config

    def start(self):
        self.login()
        self.get_trends()
        self.get_tweets_from_trends()
        self.analyze_tweets()
        self.create_news()
        self.show_page()
        self.driver.close()

    def login(self):
        login = DefaultLogin(self.driver, self.config)
        login.start()

    def get_trends(self):
        trends_scrapper = DefaultTrendsScrapper(self.driver, self.config, self.data_manager)
        trends_scrapper.start()

    def get_tweets_from_trends(self):
        tweets_scrapper = DefaultTweetsScrapper(self.driver, self.config, self.data_manager)
        tweets_scrapper.start()

    def analyze_tweets(self):
        analyzer = DefaultTweetAnalyzer(self.data_manager)
        analyzer.analyze()

    def create_news(self):
        news_maker = DefaultNewsMaker(self.config, self.data_manager)
        news_maker.start()

    def show_page(self):
        os.chdir(os.getcwd() + '/../../server')
        call(["npm", "start"])
