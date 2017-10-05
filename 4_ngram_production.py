import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from stop_words import get_stop_words
import string
import time

# set paths and filenames
data_in = '../data/toxdocs-processed-for-ngrams.p'
ngrams_out = '../data/ngrams3.p'

df = pd.read_pickle(data_in)
df = df.sample(frac=.75)
# rename columns to prevent conflict with ngram columns
df.columns = ['df1_' + str(col) for col in df.columns]

# assign unlikely dates to nan
unlikely_dates = df['df1_year'] > 2017
nonconsec_dates = df['df1_year'] < 1910
df.loc[unlikely_dates, 'df1_year'] = np.nan
df.loc[nonconsec_dates, 'df1_year'] = np.nan
df = df.dropna(subset=['df1_year'])

# update stopwords to include additional words and isolated letters
isolated_alpha = list(string.ascii_lowercase)
additional_words = ['among']
stopwords = get_stop_words('en')

stopwords.extend(isolated_alpha)
stopwords.extend(additional_words)
stopwords = sorted(stopwords)

# set tokens for vectorization
alpha_tokens = '[A-Za-z]+(?=\\s+)'

# instantiate TfidfVectorizer
vec = TfidfVectorizer(token_pattern=alpha_tokens,
                      ngram_range=(1,3),
                      analyzer='word',
                      lowercase=True,
                      stop_words = stopwords,
                      min_df=35)

# Set timer
start_time = time.clock()

# Fit to the data
ngrams = vec.fit_transform(df['df1_proctext'])
msg = "There are {} tokens in the text if we split on non-alpha"
print(msg.format(len(vec.get_feature_names())))

# Report time
print(time.clock() - start_time)


# Check shape of data before combining
ngram_names = vec.get_feature_names()
ngram_index = df.index.values
ngram_freq = np.ravel(ngrams.sum(axis=0))
print('ngrams shape: ' + str(ngrams.shape))
print('ngram_names length: ' + str(len(ngram_names)))
print('ngram_index length: ' + str(len(ngram_index)))

# combine ngrams with original dafa frame
df_ngrams = pd.DataFrame(ngrams.toarray(), index=ngram_index, columns=ngram_names)
print('\n df_ngrams.shape: ' + str(df_ngrams.shape))

df = pd.concat([df['df1_year'], df_ngrams], axis=1)
print('df.shape: ' + str(df.shape))

# remove ngrams that are two characters or less
all_cols = df.columns
short_cols = [c for c in all_cols if len(c) <= 2]
df = df.drop(short_cols, axis=1)

df.to_pickle(ngrams_out)
