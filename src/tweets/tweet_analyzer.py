import constants
from subprocess import call


class TweetAnalyzer:

    def analyze(self):
        call(["node", constants.REGEX_SCRIPT, constants.TRENDS_JSON])
