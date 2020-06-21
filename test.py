import pandas as pd
from sklearn.model_selection import train_test_split

# Replace 'training.csv' with the location of your training file
# Read in the dataset into a Pandas DataFrame
df = pd.read_csv("/Users/gabriel/PycharmProjects/GOT/training.1600000.processed.noemoticon.csv", encoding='latin-1')
# Drop unnecessary columns, leaving behind the [label, text] columns
df = df.drop(df.columns[[1, 2, 3, 4]], axis=1)

df.columns = ['label', 'text']
# Reverse the format to [text, label] as this is the standard for BERT
df = df[['text', 'label']]
df.index.name = 'index'
df = df.sample(frac = 0.5, random_state = 2020)
train, valid = train_test_split(df, test_size=0.2)

# Save back to .csv format
train.to_csv('/Users/gabriel/PycharmProjects/GOT/data/train.csv', index=False)
valid.to_csv('/Users/gabriel/PycharmProjects/GOT/data/valid.csv', index=False)
labels = ["0", "4"]
lb = pd.DataFrame(labels)
lb.to_csv('/Users/gabriel/PycharmProjects/GOT/label/labels.csv',index=False)