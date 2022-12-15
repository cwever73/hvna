#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 18:24:36 2022

Script creates a scatter plot of tfidf vs df values in bokeh.

@author: carl
"""

from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper
from bokeh.palettes import viridis
from bokeh.plotting import figure, output_file, show
from bokeh.transform import transform
import sys
import time
import yaml

def scttr_plt(x_lst, y_lst, desc_lst, title):

    output_file("../scttr_plt.html")

    source = ColumnDataSource(data=dict(x=x_lst, y=y_lst, desc=desc_lst))
    hover = HoverTool(tooltips=[
        ("(df, tfidf)", "(@x, @y)"),
        ('desc', '@desc'),])
    
    
    mapper = LinearColorMapper(palette=viridis(256), low=min(y_lst), high=max(y_lst))
    
    p = figure(width=400, height=400, tools=[hover,"box_zoom,pan,box_select,reset"], title=title, toolbar_location="below")
    p.circle('x', 'y', size=10, source=source,
             fill_color=transform('y', mapper))
    
    show(p)
    
    
if __name__ == "__main__":
    t0 = time.time()
    
    actn = sys.argv[1]
    
    if actn == 'plt_tfidf':
        
        flnm = input('Enter yaml that holds tfidf scores:  ')
        
        with open(flnm) as f:
            tfidf_dct = yaml.load(f, yaml.SafeLoader)
        
        x_lst = [tfidf_dct[tkn]['df'] for tkn in tfidf_dct]
        
        y_lst = [tfidf_dct[tkn]['tfidf'] for tkn in tfidf_dct]
        
        tkn_lst = list(tfidf_dct.keys())
        
        scttr_plt(x_lst,y_lst,tkn_lst, 'TFIDF vs DF')
            
            
    
    print(f'Script took {time.time()-t0}s to run.')