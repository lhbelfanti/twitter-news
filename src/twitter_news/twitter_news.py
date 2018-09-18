import time
from selenium import webdriver
from constants import constants
from login import Login
from trends import TrendsScrapper
from tweets import TweetsScrapper


class TwitterNews:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get(constants.TWITTER_URL)
        print(self.driver.title)

    def start(self):
        self.login()
        self.get_trends()

        time.sleep(100)
        self.driver.close()

    def login(self):
        login = Login(self.driver)
        login.start()

    def get_trends(self):
        trends_scrapper = TrendsScrapper(self.driver, self.on_trends_obtained)
        trends_scrapper.start()

    def on_trends_obtained(self, trends):
        tweets_scrapper = TweetsScrapper(self.driver, trends)
        tweets_scrapper.start()
