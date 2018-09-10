import time
from selenium import webdriver
from constants import constants
from login import Login
from trending import TrendingTopics


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
        login.login_user()

    def get_trends(self):
        trending = TrendingTopics(self.driver, self.on_trends_obtained)
        trending.start()

    def on_trends_obtained(self, trends):
        print("---")
        print(trends)
