import os
from subprocess import call
from time import sleep

import constants
from config import Configuration
from data import DataManager
from di import Injector
from driver import Driver
from logger import Logger
from login import Login
from news.maker import NewsMaker
from trends.scrapper import TrendsScrapper
from tweets.analyzer import TweetsAnalyzer
from tweets.scrapper import TweetsScrapper


class TwitterNews:
    def __init__(self):
        self._inj = Injector.get_instance()
        self._inj.load()
        self._driver = self._inj.get_service(Driver)
        self._data_manager = self._inj.get_service(DataManager)
        self._config = self._inj.get_service(Configuration)

    def start(self):
        self._open_twitter()
        self._login()
        self._define_twitter_ui_version()
        self._get_trends()
        self._get_tweets_from_trends()
        #self._analyze_tweets()
        #self._create_news()
        #self._show_page()
        #self._driver.close()

    def _open_twitter(self):
        Logger.info("Opening Twitter...")
        title = self._driver.navigate_to(constants.TWITTER_URL)
        Logger.info(title)
        Logger.info("----------------------------------------")

    def _login(self):
        login = self._inj.get_service(Login)
        login.authenticate()

    def _define_twitter_ui_version(self):
        sleep(3)
        self._config.define_twitter_ui_version(self._driver.driver.current_url)

    def _get_trends(self):
        trends_scrapper = self._inj.get_service(TrendsScrapper)
        trends_scrapper.get_trends()

    def _get_tweets_from_trends(self):
        tweets_scrapper = self._inj.get_service(TweetsScrapper)
        tweets_scrapper.get_tweets()

    def _analyze_tweets(self):
        analyzer = self._inj.get_service(TweetsAnalyzer)
        analyzer.analyze()

    def _create_news(self):
        news_maker = self._inj.get_service(NewsMaker)
        news_maker.create_news()

    def _show_page(self):
        os.chdir(os.getcwd() + constants.CLIENT_PATH)
        call(["npm", "start"])
