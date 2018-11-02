const TRENDING_TOPICS_JSON = process.argv[2];
var fs = require('fs');
var twitter = require('twitter-text');
var trendingTopics = require(TRENDING_TOPICS_JSON);

trendingTopics.forEach(function(trend) {
    trend.tweets.forEach(function(tweet) {
        tweet = analyze(tweet);
    });
});

var jsonData = JSON.stringify(trendingTopics, null, 2);

fs.writeFile(TRENDING_TOPICS_JSON, jsonData, function(err) {
    if (err) {
        console.log(err);
    }
});


function analyze(tweet) {
    tweet.text = tweet.text.replace("\n", '').replace("\r", '').replace("\t", '');

    tweet.links = twitter.extractUrls(tweet.text);
    tweet.links.forEach(function(link) {
        tweet.text = tweet.text.replace(link, '');
    });

    tweet.hashtags = twitter.extractHashtags(tweet.text);
    tweet.hashtags.forEach(function(hashtag) {
        tweet.text = tweet.text.replace("#" + hashtag, '');
    });
    
    tweet.mentions = twitter.extractMentions(tweet.text);
    tweet.mentions.forEach(function(mention) {
        tweet.text = tweet.text.replace("@" + mention, mention);
    });

    twitter.cashtags = twitter.extractCashtags(tweet.text);
    tweet.cashtags.forEach(function(cashtag) {
        tweet.text = tweet.text.replace("$" + cashtag, '');
    });
    return tweet;
}