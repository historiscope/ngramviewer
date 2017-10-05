import numpy as np
import pandas as pd
from pymongo import MongoClient

data_in = 'td'
data_out = '../data/toxdocs-clean.p'

# Function to read mongo database into pandas
def read_mongo(mongo_database, collection, query={}, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    client = MongoClient()
    db = client[mongo_database]

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df


# import data
df = read_mongo(data_in, 'documents')

# Set categorical variables
var_cats = ['case_number', 'case_title', 'document_type', 'jurisdiction', 'file_source']
[df[c].astype('category') for c in var_cats]

# pdf_dates refer to pdf processing information that is no longer valid; remove
var_pdf_dates = ['created_at', 'date_filed', 'date_terminated', 'updated_at']
df = df.drop(var_pdf_dates, axis=1)

# Remove whitespace in the document text and set resulting empty fields as nan
df['proctext'] = df['text'].str.replace(r'\s+', ' ')
df['proctext'] = df['proctext'].str.replace(r'^\s+|\s+?$', '')

# set blanks as missing values
df['proctext'] = df['proctext'].replace('', np.nan)

# Remove rows with missing data on text
df = df.dropna(subset=['proctext'])

print(df.shape)

df.to_pickle(data_out)
