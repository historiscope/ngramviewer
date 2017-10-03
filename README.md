# N-gram Timeline Viewer

I produced this visualization as part of a consulting project with ToxicDocs.org, an online repository of previously secret documents about toxic contamination that became public through corporate litigation. After placing more than four million pages of documents online, ToxicDocs was seeking tools that would offer site visitors different ways to interact with the collection. Specifically, they asked me to create an N-gram Timeline Viewer, similar to those created by [Google](https://books.google.com/ngrams) and (FiveThirtyEight)[https://projects.fivethirtyeight.com/reddit-ngram/].

__The Data__

To produce the data for the plots, I imported the documents (already OCRed) from a MongoDB database into Pandas and created unigrams, bi-grams, and tri-grams using the NLTK library, after cleaning and pre-processing the text to remove unwanted text and characters (stopwords, punctuation, email addresses, etc.).

In addition, I improved upon the estimated dates. Only a small fraction of the documents in the repository have any date associated with them: an estimated year. As this was clearly a problem for a timeline, I used [Datefinder](http://datefinder.readthedocs.org/en/latest/) to estimate the month, day, and year of the documents. This doubled the number of documents with dates, and offered more temporal precision.

__The Plot__

I selected the [Bokeh library](https://bokeh.pydata.org) to produce the online visualization. Like D3, Bokeh offers interactive features for web-based plots, including panning, zooming, and autocomplete text. Unlike D3, Bokeh plots can be created using Python and R as well as JavaScript, giving my client greater flexibility moving forward. In addition, custom JavaScript can be added to plots produced using Python or R, which offers many options for customizing the plot.

To create the Bokeh plot, I grouped the data by year and converted the data to Bokeh's ColumnDataSource format to take full advantage of Bokeh's interactive capability. I used _multi_line_,  _AutoCompleteInput_, and created a callback function to redraw the plot when the user entered new terms into the input box. Once it was created, I embedded the plot in an html template and used Bokeh Server to run in the background on AWS, making it possible for site visitors to access and interact with the plot.

__Future Plans__

The plot will go live on the tools section of the [ToxicDocs.org website](https://www.toxicdocs.org) when they unveil their new site sometime in the next few months. I have a few improvements in mind in the meantime. First, I'd like to prune the n-grams, eliminating those with very low frequency based on a histogram, and also using Parts-Of-Speech identification to screen for nonsensical phrases (an adjective following a noun, for example). In addition, I'm keeping an eye on where Bokeh heads with its _AutoCompleteInput_ function. Autocomplete is a great feature for a repository of this sort, as it educates site visitors about the content as they search.  But this particular function is a little buggy and the formatting of the look-up list is less than ideal. _AutoCompleteInput_ is under active development in Bokeh, so it's worthwhile to wait and see where it goes, but a custom JavaScript function may be in order.