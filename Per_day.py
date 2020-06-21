from StockScraper import *
from TweetScraper import *
from datetime import datetime, timedelta, time

def Per_day(ticker = "TSLA"):
    dir_path = '/Users/gabriel/PycharmProjects/GOT/Data/Tweets'
    opener  = time.fromisoformat('09:30:00')
    closer  = time.fromisoformat('16:00:00')
    Stock = []
    Stock_later = []
    #Stock Info
    path, name = to_json(ticker, '2018-09-10', '2020-06-10', '1h')
    json_to_csv(path, name)
    stock_df = pd.read_csv(os.getcwd() + "/Data/Clean_ticker_data/" + name + ".csv")
    stock_df['Time'] = [d[0:19] for d in stock_df['Time']]
    stock_df['Time'] = pd.to_datetime(stock_df['Time'])
    stock_df['Time'] = stock_df['Time'].dt.to_pydatetime()
    stock_df.set_index('Time', inplace = True)
    master_df = pd.DataFrame(columns=['Date','Username','Retweets','Likes','Tweets','Stock at 9:30','Stock at 4:00'])
    cnt = 0
    for i, filename in enumerate(os.listdir(dir_path)):
        if filename[0] == 'T':
            df = pd.read_csv(dir_path + '/' + filename)
            cnt += df.shape[0]
            for i, row in df.iterrows():
                timestamp = datetime.strptime(row["Date"][0:18], '%Y-%m-%d %H:%M:%S')
                if (timestamp.weekday() < 5) and (opener <  timestamp.time()) and (timestamp.time() < closer):
                    start_time = datetime.combine(timestamp.date(),opener)
                    end_time = datetime.combine(timestamp.date(),time.fromisoformat('15:30:00'))
                    master_df = master_df.append(row)
                    Stock.append(stock_df.iloc[stock_df.index.get_loc(start_time, method='nearest')]['Open'])
                    Stock_later.append(stock_df.iloc[stock_df.index.get_loc(end_time, method='nearest')]['Close'])
    master_df['Stock at 9:30'] = Stock
    master_df['Stock at 4:30'] = Stock_later
    final_file_path = os.getcwd() + '/Data/TSLA_Daily/' + '20Month_Clean_GroupByDay' + ".csv"
    master_df.to_csv(final_file_path, index=False)
    print("Went from ", cnt, " to ", master_df.shape[0])


def per_hour(ticker = "TSLA"):
    dir_path = '/Users/gabriel/PycharmProjects/GOT/Data/Tweets'
    opener = time.fromisoformat('09:30:00')
    closer = time.fromisoformat('16:00:00')
    Stock = []
    Stock_later = []
    #Stock Info
    path, name = to_json(ticker, '2018-09-10', '2020-06-10', '1h')
    json_to_csv(path, name)
    stock_df = pd.read_csv(os.getcwd() + "/Data/Clean_ticker_data/" + name + ".csv")
    stock_df['Time'] = [d[0:19] for d in stock_df['Time']]
    stock_df['Time'] = pd.to_datetime(stock_df['Time'])
    stock_df['Time'] = stock_df['Time'].dt.to_pydatetime()
    print(type(stock_df['Time'][0]))
    stock_df.set_index('Time', inplace = True)
    master_df = pd.DataFrame(columns=['Date','Username','Retweets','Likes','Tweets','Stock at 9:30','Stock at 4:00'])
    cnt = 0
    for i, filename in enumerate(os.listdir(dir_path)):
        if filename[0] == 'T':
            df = pd.read_csv(dir_path + '/' + filename)
            cnt += df.shape[0]
            for i, row in df.iterrows():
                timestamp = datetime.strptime(row["Date"][0:18], '%Y-%m-%d %H:%M:%S')
                if (timestamp.weekday() < 5) and (opener < timestamp.time()) and (timestamp.time() < closer):
                    if timestamp.time().minute <= 30: #round down
                        start_hour = time.fromisoformat(str(timestamp.time().hour - 1).zfill(2) + ':30:00')
                        end_hour = time.fromisoformat(str(timestamp.time().hour).zfill(2) + ':30:00')
                        start_time = datetime.combine(timestamp.date(),start_hour)
                        end_time = datetime.combine(timestamp.date(), end_hour)
                    if timestamp.time().minute > 30: #you are good
                        start_hour = time.fromisoformat(str(timestamp.time().hour).zfill(2) + ':30:00')
                        end_hour = time.fromisoformat(str(timestamp.time().hour + 1).zfill(2) + ':30:00')
                        start_time = datetime.combine(timestamp.date(),start_hour)
                        end_time = datetime.combine(timestamp.date(), end_hour)
                    master_df = master_df.append(row)
                    Stock.append(stock_df.iloc[stock_df.index.get_loc(start_time, method='nearest')]['Open'])
                    Stock_later.append(stock_df.iloc[stock_df.index.get_loc(end_time, method='nearest')]['Close'])
    master_df['Stock at 9:30'] = Stock
    master_df['Stock at 4:30'] = Stock_later
    final_file_path = os.getcwd() + '/Data/TSLA_Daily/' + '20Month_Clean_GroupByHour' + ".csv"
    master_df.to_csv(final_file_path, index=False)
    print("Went from ", cnt, " to ", master_df.shape[0])

per_hour()