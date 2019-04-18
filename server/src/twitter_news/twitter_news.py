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
        self._inj = injector
        self._driver = self._inj.get_service(Driver)
        self._data_manager = self._inj.get_service(DataManager)
        self._config = self._inj.get_service(Configuration)

    def start(self):
        self._open_twitter()
        self._login()
        self._get_trends()
        self._get_tweets_from_trends()
        self._analyze_tweets()
        self._create_news()
        self._show_page()
        self._driver.close()

    def _open_twitter(self):
        Logger.info("Opening Twitter...")
        title = self._driver.navigate_to(constants.TWITTER_URL)
        Logger.info(title)
        Logger.info("----------------------------------------")

    def _login(self):
        login = self._inj.get_service(Login)
        login.login_user()

    def _get_trends(self):
        trends_scrapper = self._inj.get_service(TrendsScrapper)
        trends_scrapper.get_trends()

    def _get_tweets_from_trends(self):
        tweets_scrapper = self._inj.get_service(TweetsScrapper)
        tweets_scrapper.get_tweets()

    def _analyze_tweets(self):
        analyzer = self._inj.get_service(TweetAnalyzer)
        analyzer.analyze()

    def _create_news(self):
        news_maker = self._inj.get_service(NewsMaker)
        news_maker.create_news()

    def _show_page(self):
        os.chdir(os.getcwd() + constants.SERVER_PATH)
        call(["npm", "start"])
