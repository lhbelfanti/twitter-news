from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriverCreator:
    def __init__(self):
        # Load the Chrome webdriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

        # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads
        # and put it as an environment variable
        self._driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver")

    @property
    def driver(self):
        return self._driver
