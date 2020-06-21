from StockScraper import *
from TweetScraper import *
from datetime import datetime, timedelta
import time


class dataset_collection:
    def __init__(self, search_words,stock, start_date, end_date, interval, max_tweets, file_name, type):
        self.query = search_words
        self.ticker = stock
        self.since = start_date
        self.end = end_date
        self.max_tweets = max_tweets
        self.t_file_name = file_name
        self.interval = interval
        self.type = type
    def datetime_conv(self, df):
        df['Time'] = datetime.strptime(df['Time'][0:18],'%Y-%m-%d %H:%M:%S')
        return df

    def collect(self, minlikes, minreplies, minretweets):
        #Collect the Tweets and writes it to a CSV file in Data/Tweets
        get_tweets(self.query,self.since, self.end, self.max_tweets, self.t_file_name, minlikes, minreplies, minretweets)
        #loading it as a dataframe
        tweet_df = pd.read_csv(os.getcwd() + "/Data/Tweets/" + self.t_file_name + ".csv")
        #Collecting Stock data from Yahoo finance and saving it to a JSON file in Data/Raw_json
        path, name = to_json(self.ticker, self.since, self.end, self.interval)
        #Converting JSON file into readable CSV file of stock data in Data/Clean_ticker_data
        json_to_csv(path, name, self.end)
        #loading it as a dataframe
        stock_df = pd.read_csv(os.getcwd() + "/Data/Clean_ticker_data/" + name + ".csv")
        Stock = []
        Stock_later = []
        #Converting stock time from string to datetime
        stock_df['Time'] = pd.to_datetime(stock_df['Time'])
        stock_df['Time'] = stock_df['Time'].dt.to_pydatetime()
        #Convert the Time column into the index (zzzzzz was an issue for 5 fucking hours
        stock_df.set_index('Time', inplace = True)
        # iterating through all tweet
        for i, row in tweet_df.iterrows():
            #Time of Tweet
            tweet_time = datetime.strptime(row["Date"][0:18],'%Y-%m-%d %H:%M:%S')
            # Get Ticker price that is closest to the time of posting the tweet, and the price 5 minutes later
            Stock.append(stock_df.iloc[stock_df.index.get_loc(tweet_time, method='nearest')][self.type])
            Stock_later.append(stock_df.iloc[stock_df.index.get_loc(tweet_time + timedelta(hours = 1),method='nearest')][self.type])
        tweet_df['Stock at T'] = Stock
        tweet_df['Stock at T+1'] = Stock_later
        #print(tweet_df.head(3))
        final_file_path = os.getcwd() + '/Data/Final_actual_test/' + self.t_file_name + ".csv"
        tweet_df.to_csv(final_file_path, index=False)
        print("Finished Writing Final dataframe to CSV file.... \n")

Query = "TESLA OR TSLA"
Ticker = "TSLA"
freq = "1h"
max_tweets = 35000
stock_type = "Close"
Min_likes = 75
min_replies = 10
min_retweets = 10
dates = ['2020-06-10','2020-05-10','2020-04-10','2020-03-10','2020-02-10','2020-01-10',
         '2019-12-10','2019-11-10','2019-10-10','2019-09-10','2019-08-10','2019-07-10','2019-06-10','2019-05-10','2019-04-10',
         '2019-03-10','2019-02-10','2019-01-10', '2018-12-10', '2018-11-10', '2018-10-10','2018-09-10']
month = ['May2020', 'April2020', 'March2020','February2020','January2020','December2019','November2019','October2019',
         'September2019', 'August2019', 'June2019', 'May2019','April2019', 'March2019','February2019', 'January2019',
         'December2018','November2018', 'October2018', 'September2018','August2018']
for i in range(0,len(dates)):
    start = dates[i+1]
    end = dates[i]
    file_name = "high_constraint_TESLA_Test" + month[i]
    get_tweets(Query, start, end, max_tweets, file_name, Min_likes, min_replies, min_retweets)
    time.sleep(15*60)










