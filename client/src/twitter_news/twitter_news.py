import os
from subprocess import call

import constants
from config import Configuration
from data import DataManager
from driver import Driver
from logger import Logger
from login import Login
from news.maker import NewsMaker
from trends.scrapper import TrendsScrapper
from tweets.analyzer import TweetAnalyzer
from tweets.scrapper import TweetsScrapper


class TwitterNews:
    def __init__(self, injector):
        self.inj = injector
        self.driver = self.inj.get_service(Driver)
        Logger.info("Opening Twitter...")
        title = self.driver.navigate_to(constants.TWITTER_URL)
        Logger.info(title)
        Logger.info("----------------------------------------")
        self.data_manager = self.inj.get_service(DataManager)
        self.config = self.inj.get_service(Configuration)

    def start(self):
        self.login()
        self.get_trends()
        self.get_tweets_from_trends()
        self.analyze_tweets()
        self.create_news()
        self.show_page()
        self.driver.close()

    def login(self):
        login = self.inj.get_service(Login)
        login.start()

    def get_trends(self):
        trends_scrapper = self.inj.get_service(TrendsScrapper)
        trends_scrapper.start()

    def get_tweets_from_trends(self):
        tweets_scrapper = self.inj.get_service(TweetsScrapper)
        tweets_scrapper.start()

    def analyze_tweets(self):
        analyzer = self.inj.get_service(TweetAnalyzer)
        analyzer.analyze()

    def create_news(self):
        news_maker = self.inj.get_service(NewsMaker)
        news_maker.start()

    def show_page(self):
        os.chdir(os.getcwd() + '/../../server')
        call(["npm", "start"])
