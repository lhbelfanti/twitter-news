import sys
import twitter_news
import constants
from config import Configuration
from logger import Logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


Logger.load()
args = sys.argv
config_file = ""
if len(args) != 3:
    Logger.error("Twitter's user and password needed")
    Logger.error("USAGE: python3 start.py <TWITTER_USER> <TWITTER_PASSWORD>")
    exit(1)
else:
    constants.USERNAME = args[1]
    constants.PASSWORD = args[2]


# Load the Chrome webdriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

# download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it as an
# environment variable
chrome_driver = "chromedriver"
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

# Load config
Configuration.load()

# Start the app
twitter = twitter_news.TwitterNews(driver)
twitter.start()

