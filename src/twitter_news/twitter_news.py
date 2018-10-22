import time
from selenium import webdriver
import utils
import constants
from login import Login
from trends import TrendsScrapper
from tweets import TweetsScrapper


class TwitterNews:
    def __init__(self):
        utils.log("Opening Twitter...")
        self.driver = webdriver.Chrome()
        self.driver.get(constants.TWITTER_URL)
        utils.log(self.driver.title)
        utils.log("----------------------------------------")

    def start(self):
        self.login()
        self.get_trends()
        self.driver.close()

    def login(self):
        utils.log("Logging in...")
        login = Login(self.driver)
        login.start()
        utils.log("----------------------------------------")

    def get_trends(self):
        utils.log("Getting trends...")
        trends_scrapper = TrendsScrapper(self.driver, self.on_trends_obtained)
        trends_scrapper.start()

    def on_trends_obtained(self, trends):
        utils.log("Getting tweets...")
        tweets_scrapper = TweetsScrapper(self.driver, trends)
        tweets_scrapper.start()
        utils.log("----------------------------------------")
        utils.log("Saving to json...")
        tweets_scrapper.save_to_json()
        utils.log("----------------------------------------")
