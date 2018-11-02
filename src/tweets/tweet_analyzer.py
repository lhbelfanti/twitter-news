import constants
import re
from subprocess import call



class TweetAnalyzer:

    def __init__(self):
        self.tweet = None

    def analyze(self):
        call(["node", constants.REGEX_SCRIPT, constants.TRENDS_JSON])

