import constants
from selenium import webdriver
from logger import Logger
from login import Login
from trends import TrendsScrapper
from tweets import TweetsScrapper
from tweets import TweetAnalyzer
from news import NewsMaker


class TwitterNews:
    def __init__(self):
        Logger.info("Opening Twitter...")
        self.driver = webdriver.Chrome()
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
        trends_scrapper.start()

    def on_trends_obtained(self, trends):
        Logger.info("Getting tweets...")
        tweets_scrapper = TweetsScrapper(self.driver, trends)
        tweets_scrapper.start()
        Logger.info("----------------------------------------")
        Logger.info("Saving to json...")
        tweets_scrapper.save_to_json()
        Logger.info("----------------------------------------")
        self.analyze_tweets()

    def analyze_tweets(self):
        Logger.info("Analyzing tweets...")
        Logger.info("----------------------------------------")
        analyzer = TweetAnalyzer()
        analyzer.analyze()
        Logger.info("----------------------------------------")
        self.create_news()

    def create_news(self):
        Logger.info("Creating news...")
        Logger.info("----------------------------------------")
        news_maker = NewsMaker()
        news_maker.start()
        Logger.info("----------------------------------------")
