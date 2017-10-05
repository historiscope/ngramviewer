import pandas as pd

data_in = '../data/toxdocs-clean.p'
data_ngrams_out = '../data/toxdocs-processed-for-ngrams.p'

df = pd.read_pickle(data_in)
print(df.info())

# creating field for processed text
df['proctext'] = df['text']

# Remove punctuation
df['proctext'] = df['proctext'].str.replace(r'[^\w\d\s]', ' ')

# Replace email addresses with 'emailaddr'
df['proctext'] = df['proctext'].str.replace(r'\b[\w\-.]+?@\w+?\.\w{2,4}\b', 'emailaddr')

print('saving data for ngrams')
df.to_pickle(data_ngrams_out)

print(df.info())
