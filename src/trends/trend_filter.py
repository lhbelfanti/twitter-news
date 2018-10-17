import time
import utils
import constants
from exceptions import LoadingTimeout
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException


class TrendFilter:
    def __init__(self, driver, trend):
        self.driver = driver
        self.trend = trend
        self.stream_items = None
        self.filter_container = None
        self.select_element = None
        self.current_filter = 0

    def start(self):
        self.open_trend(self.trend.url)  # Change it with the already formatted url to avoid refreshing the page
        self.click_show_filter()
        self.process_filters()

    def open_trend(self, url):
        self.driver.get(url)
        self.load_stream_items(constants.WAIT_PAGE_LOAD)

    def load_stream_items(self, sleepTime):
        try:
            self.stream_items = utils.wait_until_load(By.CLASS_NAME, constants.TWEETS_LIST, self.driver)
            time.sleep(sleepTime)
        except TimeoutException:
            raise LoadingTimeout()

    def click_show_filter(self):
        self.filter_container = utils.get_element_by(By.CLASS_NAME, constants.FILTER_CONTAINER, self.driver)
        filter_button = utils.get_element_by(By.CLASS_NAME, constants.FILTER_BUTTON, self.filter_container)
        filter_button.click()

    def process_filters(self):
        filters = utils.get_elements_by(By.CLASS_NAME, constants.FILTERS, self.filter_container)
        index = 0
        for filter_item in filters:
            if self.current_filter == index:
                self.current_filter += 1
                # Get filter type
                filter_type = filter_item.get_attribute(constants.FILTER_ATTRIBUTE)
                # Get 'select' element
                self.select_element = Select(utils.get_element_by(By.CLASS_NAME, constants.FILTER_SELECT, filter_item))
                # Choose 'select' option by filter type
                default_option = self.select_filter(filter_type)

                if not default_option:  # Don't want to reload the page if the default option is selected
                    break
            index += 1

    def select_filter(self, filter_type):
        if filter_type == constants.FILTER_BY_SOCIAL:
            return True  # Using the default (From anyone) option
        elif filter_type == constants.FILTER_BY_LOCATION:
            self.select_element.select_by_visible_text(constants.FILTER_BY_LOCATION_OPTION)
            self.on_page_refresh()
        elif filter_type == constants.FILTER_BY_LANGUAGE:
            self.select_element.select_by_visible_text(constants.FILTER_BY_LANGUAGE_OPTION)
            self.on_page_refresh()
        elif filter_type == constants.FILTER_BY_QUALITY:
            return True  # Using the default (Quality filter on) option

        return False

    def on_page_refresh(self):
        time.sleep(constants.WAIT_REFRESH)
        self.load_stream_items(0)
        self.filter_container = utils.get_element_by(By.CLASS_NAME, constants.FILTER_CONTAINER, self.driver)
        self.process_filters()
