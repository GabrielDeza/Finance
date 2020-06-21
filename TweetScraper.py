import GetOldTweets3 as got
import time
import os
import csv

def get_tweets(keyword, start_date, end_date, max_tweets, file_name, L,Replies,Retweets):
    """
    :param keyword: Keywords relevant to the tweets you wish to get (abc OR
    :param start_date: Lower bound on tweets to scrape from (YYYY-MM-DD)
    :param end_date: Upper bound on tweets to scrape from (YYYY-MM-DD)
    :param max_tweets: Maximum Number of Tweets to be retrieved. if None, retrieve all tweets.
    :param file_name: file name for the csv file within the data folder
    :return: Boolean
    """
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword)\
                                                .setSince(start_date)\
                                                .setUntil(end_date)\
                                                .setLang("en")\
                                                .setMinFaves(str(L))\
                                                .setMinRetweets(str(Retweets))\
                                                .setMinReplies(str(Replies))\
                                                .setMaxTweets(max_tweets)

    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    with open(os.getcwd() + "/Data/important/" + file_name + ".csv", "w", encoding = "utf-8") as csvfile:
        fieldnames = ["Date","Username", "Retweets", "Likes", "Tweet"]
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames, lineterminator = "\n")
        writer.writeheader()
        for tweet in tweets:
            writer.writerow({"Date": tweet.date,
                             "Username": str(tweet.username),
                             "Retweets": tweet.retweets,
                             "Likes": tweet.favorites,
                             "Tweet": str(tweet.text)})
        print('\n Requested {} Tweets and {} satisfied the constraints...'.format(max_tweets,len(tweets)))

