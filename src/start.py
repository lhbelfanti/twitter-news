import sys
import twitter_news
import constants

args = sys.argv
if len(args) != 3:
    print("Twitter's user and password needed")
    exit(1)
else:
    constants.USERNAME = args[1]
    constants.PASSWORD = args[2]


twitter = twitter_news.TwitterNews()
twitter.start()
