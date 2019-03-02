import constants
import os
from subprocess import call
from logger import Logger
from login import Login
from trends import TrendsScrapper
from tweets import TweetsScrapper
from tweets import TweetAnalyzer
from news import NewsMaker


class TwitterNews:
    def __init__(self, driver):
        Logger.info("Opening Twitter...")
        self.driver = driver
        self.driver.get(constants.TWITTER_URL)
        Logger.info(self.driver.title)
        Logger.info("----------------------------------------")

    def start(self):
        self.login()
        self.get_trends()
        self.driver.close()

    def login(self):
        Logger.info("Logging in...")
        login = Login(self.driver)
        login.start()
        Logger.info("----------------------------------------")

    def get_trends(self):
        Logger.info("Getting trends...")
        trends_scrapper = TrendsScrapper(self.driver, self.on_trends_obtained)
        Logger.info("----------------------------------------")
        trends_scrapper.start()

    def on_trends_obtained(self, trends):
        Logger.info("Getting tweets...")
        tweets_scrapper = TweetsScrapper(self.driver, trends)
        tweets_scrapper.start()
        Logger.info("----------------------------------------")
        self.analyze_tweets(tweets_scrapper.trending_topics)

    def analyze_tweets(self, trending_topics):
        Logger.info("Analyzing tweets...")
        analyzer = TweetAnalyzer(trending_topics)
        analyzer.analyze()
        Logger.info("----------------------------------------")
        self.create_news(analyzer.trending_topics)

    def create_news(self, trending_topics):
        Logger.info("Creating news...")
        news_maker = NewsMaker(trending_topics)
        news_maker.start()
        Logger.info("----------------------------------------")
        self.show_page()

    def show_page(self):
        os.chdir(os.getcwd() + '/../../server')
        call(["npm", "start"])
