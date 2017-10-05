#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 12:29:22 2017

@author: ruth
"""

import datefinder
import pandas as pd
from nltk import sent_tokenize
from datetime import datetime

data_in = '../data/toxdocs-clean.p'
data_out = '../data/toxdocs-clean-dates.p'

start_date = datetime(1900, 1, 1)
end_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

df = pd.read_pickle(data_in)

corpus = df['proctext']

# verify that date is legitimate (after 1900 but before today)
def check_date(d, start_d, end_d):
    date_status = start_d < d < end_d
    return date_status


# Create a function to identify and return the first legitimate date that 
# appears in the first n lines of each document. If no such date exists, check  
# the last ten lines of the document for a legitimate date and return that.
def get_est_date(self, start_d, end_d = datetime.today(), 
                 n_first=10, n_last=10, strictness=True):
    # tokenize text by sentence
    sentences = sent_tokenize(self)
    # check to see if there's a date in the first n lines
    selection = ' '.join(sentences[0:n_first])
    dates = datefinder.find_dates(selection, strict=strictness)
    # convert datefinder object to a list of dates
    dates = [d.replace(hour=0, minute=0, second=0, microsecond=0).replace(tzinfo=None) for d in dates]
    # verify dates are legitimate
    legit_dates = [d for d in dates if check_date(d, start_d, end_d) == True]
    # if any legitimate date exists in the first n lines, return the first one
    if len(legit_dates) > 0:
        return legit_dates[0]
    # if not repeat the process with the last n lines in the document
    slice = (n_last * -1) - 1
    selection = ' '.join(sentences[slice:-1])
    dates = datefinder.find_dates(selection, strict=strictness)
    # convert datefinder object to a list of dates
    dates = [d.replace(hour=0, minute=0, second=0, microsecond=0).replace(tzinfo=None) for d in dates]
    # verify dates are legitimate
    legit_dates = [d for d in dates if check_date(d, start_d, end_d) == True]
    # if any legitimate date exists in the first n lines, return the first one
    if len(legit_dates) > 0:
        # if there is, return the first date from the first ten sentences
        return legit_dates[0]
    else: 
        return None
    

# process the corpus to retrieve estimated dates
df['est_date'] = corpus.apply(get_est_date, start_d = start_date)

# save data locally
df.to_pickle(data_out)


