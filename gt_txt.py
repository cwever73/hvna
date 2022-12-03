#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 14:06:11 2022

Script gets text from desired urls.

@author: carl
"""

from bs4 import BeautifulSoup as btflSp
from datetime import datetime as dt
import requests
import time


def gt_urls():
    '''func to grab urls to search from news sites'''
    
    #for npr specifically
    url = 'https://text.npr.org'
    reqs = requests.get(url)
    soup = btflSp(reqs.text, 'html.parser')
    
    npr_url_lst = []
    for indx, link in enumerate(soup.find_all('a')):
        if indx == 0:
            og_link = link.get('href')
        elif link.get('href') is not None:
            print(link.get('href'))
            nw_url = og_link[:-1] + link.get('href')
            npr_url_lst.append(nw_url)
            
    npr_url_lst = list(set(npr_url_lst))
    print(npr_url_lst)
    
    #for nyt specifically
    url = 'https://www.nytimes.com/timeswire'
    reqs = requests.get(url)
    soup = btflSp(reqs.text, 'html.parser')
    
    tdy_dt_str = dt.today().strftime('%Y/%m/%d')
    
    nyt_url_lst = []
    for indx, link in enumerate(soup.find_all('a')):
        if link.get('href') is not None:
            if tdy_dt_str in link.get('href'):
                print(link.get('href'))
                nw_url = 'https://www.nytimes.com' + link.get('href')
                nyt_url_lst.append(nw_url)
            
    nyt_url_lst = list(set(nyt_url_lst))
    print(nyt_url_lst)
    
    
    #for cnn specifically
    url = 'https://lite.cnn.com/en'
    reqs = requests.get(url)
    soup = btflSp(reqs.text, 'html.parser')
    
    tdy_dt_str = dt.today().strftime('%Y/%m/%d')
    
    cnn_url_lst = []
    for indx, link in enumerate(soup.find_all('a')):
        if link.get('href') is not None:
            print(link.get('href'))
            nw_url = 'https://lite.cnn.com' + link.get('href')
            cnn_url_lst.append(nw_url)
            
    cnn_url_lst = list(set(cnn_url_lst))
    print(cnn_url_lst)
    
    
    #catch all
    url = 'https://skimfeed.com/news.html'
    reqs = requests.get(url)
    soup = btflSp(reqs.text, 'html.parser')

    skmfd_url_lst = []
    for indx, link in enumerate(soup.find_all('a')):
        if link.get('href') is not None:
            if 'r.php' in link.get('href') and 'www' in link.get('href'):
                nw_url = 'https://www' + link.get('href').split('www')[1]
                nw_url = nw_url.replace('%2F', '/')
                skmfd_url_lst.append(nw_url)
            
    skmfd_url_lst = list(set(skmfd_url_lst))
    print(skmfd_url_lst)
    
    
    return list(set(npr_url_lst+nyt_url_lst+cnn_url_lst+skmfd_url_lst))


def gt_txt():
    '''func to get text from each url of interest'''
    
if __name__ == "__main__":
    t0 = time.time()
    
    total_url_lst = gt_urls()
    
    print(f'Script took {time.time()-t0}s to run.')
    
