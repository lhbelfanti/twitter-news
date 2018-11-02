import json
import time
import io
import utils
import constants
from exceptions import ElementNotFound
from logger import Logger
from tweets import Tweet
from trends import TrendFilter
from selenium.webdriver.common.by import By


class TweetsScrapper:
    def __init__(self, driver, trends_data):
        self.driver = driver
        self.trends_data = trends_data
        self.stream_items = None
        self.trending_topics = []

    def start(self):
        i = 0
        for trend in self.trends_data:
            i = 1
            Logger.info("---------- From " + trend.title + ": ----------")
            trend_filter = TrendFilter(self.driver, trend)
            trend_filter.start()
            self.stream_items = trend_filter.stream_items
            self.scroll_to_bottom(constants.TIMES_TO_SCROLL_TO_BOTTOM)
            self.get_tweets(trend)
            if i == 1:
                break

    def scroll_to_bottom(self, times):
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for i in range(0, times):
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(constants.SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_tweets(self, trend):
        tweets_obj = utils.get_elements_by(By.CLASS_NAME, constants.TWEET_ITEM, self.stream_items)
        for tweet_obj in tweets_obj:
            tweet_data = utils.get_element_by(By.CLASS_NAME, constants.TWEET, tweet_obj)
            tweet_user = utils.get_element_by(By.CLASS_NAME, constants.TWEET_USER, tweet_data)
            user = tweet_user.get_attribute(constants.LINK_TAG)
            tweet_text = utils.get_element_by(By.CLASS_NAME, constants.TWEET_TEXT, tweet_data)
            text = tweet_text.text
            images = []
            Logger.info(text)
            try:
                media_container = utils.get_element_by(By.CLASS_NAME, constants.MEDIA_CONTAINER, tweet_data)
                tweet_images = utils.get_elements_by(By.TAG_NAME, constants.IMG_TAG, media_container)
                for img in tweet_images:
                    image = img.get_attribute(constants.SRC_TAG)
                    image = image.replace("'", "")
                    images.append(image)
            except ElementNotFound:
                Logger.info("The tweet doesn't contain any image")

            user = user.replace("'", "")
            tweet = Tweet(user, text, images)
            trend.tweets.append(tweet.__dict__)
        self.trending_topics.append(trend.__dict__)

    def save_to_json(self):
        with io.open(constants.TRENDS_JSON, 'w', encoding='utf8') as json_file:
            data = json.dumps(self.trending_topics, ensure_ascii=False, indent=4)
            json_file.write(data)

        Logger.info("Data saved successfully!")