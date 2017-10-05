from bokeh.io import curdoc
from bokeh.layouts import column, row, widgetbox
from bokeh.models import AutocompleteInput, Button, ColumnDataSource
from bokeh.palettes import Spectral11
from bokeh.plotting import figure
from bokeh.themes import Theme

from import_data import df

Theme('static/bokeh/theme.yaml')

# group data & create columns for CDS
group = df.groupby('df1_year').mean()

# get lookup list for ngrams
lookup_list = list(group.columns)

# instantiate the variable lists for use with ColumnDataSource
x = []
y = []

# start with any n-gram to establish data for a hidden multi_line glyph
ngrams = [lookup_list[0]]
        
for ngram in ngrams:
    y.append(group[ngram])
    x.append(group.index.values)

# Create initial ColumnDataSource
source = ColumnDataSource(data=dict(x=x, 
                                    y=y,
                                    labels=ngrams, 
                                    colors=Spectral11[0:len(ngrams)]))

# set up figure
p = figure(plot_width=700, plot_height=400)

# set up multi_line structure then hide that and the legend
main_line = p.multi_line('x', 'y', source=source, 
             line_width=3, line_join='bevel', line_color='colors', 
              alpha=0.9, legend='labels')
main_line.visible = False
p.legend.visible = False

# hide the yaxis as values are meaningless here
p.yaxis.visible = False

new_ngrams = []
# set up callback: update_plot
def update_plot(attr, old, new):
    global group, lookup_list, new_ngrams
    mycheck = True
    try:
        group[new]
    except KeyError:
        print('no such word or phrase in ngram list')
        mycheck = False
    if mycheck:
    #finally:
        print('wtf')
        xlist = []
        ylist = []
        new_ngrams.append(box.value)
        
        # redo lookup_list to exclude terms that have already been plotted
        lookup_list = [x for x in lookup_list if x not in new_ngrams]
    
        numlines = len(new_ngrams)
        colors = Spectral11[0:numlines]
    
        # set up x and y
        for ngram in new_ngrams:
            ylist.append(group[ngram])
            xlist.append(group.index.values)
    
        # replace CDS values  
        source.data = {'x': xlist,
                       'y': ylist,
                       'colors': colors,
                       'labels': new_ngrams
                       }
        main_line.visible = True
        p.legend.visible = True

def clear_lines():
    global new_ngrams, lookup_list, box
    new_ngrams = []
    main_line.visible = False
    p.legend.visible = False
    lookup_list = list(group.columns)

# set up autocomplete box and trigger
box = AutocompleteInput(completions=lookup_list, placeholder='Enter text')
#box = TextInput(placeholder='Enter text')
box.on_change('value', update_plot)

clear = Button(label='clear all lines')
clear.on_click(clear_lines)

# create layout
box_widget = widgetbox(box)
clear_widget = widgetbox(clear)
layout = column(p, row(box_widget, clear_widget))
curdoc().add_root(layout)
