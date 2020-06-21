import pandas as pd

# Replace 'training.csv' with the location of your training file
# Read in the dataset into a Pandas DataFrame
df = pd.read_csv("/Users/gabriel/PycharmProjects/GOT/training.1600000.processed.noemoticon.csv", encoding='latin-1')

# Drop unnecessary columns, leaving behind the [label, text] columns
df = df.drop(df.columns[[1, 2, 3, 4]], axis=1)

# Rename these columns
df.columns = ['label', 'text']

# Reverse the format to [text, label] as this is the standard for BERT
df = df[['text', 'label']]
df.index.name = 'index'
df = df.sample(frac = 0.5, random_state = 2020)


filename = '/Users/gabriel/PycharmProjects/GOT/sentiment140compressed.h5'


store = pd.HDFStore("hopeful.h5")
store['data'] = df
store.close()

#df.to_hdf(filename, 'data', mode='w')