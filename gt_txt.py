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
import sys
import time
from txt_anlyss import Tokenize


def gt_ggl_urls(srch_trm):
    '''func to grab urls from a particular google search'''
    
    srch_trm = srch_trm.replace(' ', '+')
    url = f'https://www.google.com/search?q={srch_trm}'
    print(f'URL: {url}')
    reqs = requests.get(url)
    soup = btflSp(reqs.text, 'html.parser')
    
    ggl_url_lst = []
    for indx, link in enumerate(soup.find_all('a')):
        print(indx, link.get('href'))
        if '/url?q=' in link.get('href'):
            nw_url = link.get('href').split('/url?q=')[1]
            ggl_url_lst.append(nw_url)
    
    print(ggl_url_lst)
    
    return ggl_url_lst

    
def gt_nws_urls():
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


def gt_txt(url_lst):
    '''Given a list of urls, return a list of dictionaries
     containin url and respective text from each'''
    
    url_txt = []
    
    for url in url_lst:
        reqs = requests.get(url)
        soup = btflSp(reqs.text, 'html.parser')
        
        if 'Error 404' in soup.text:
            print(f'Invalid url: {url}')
        else:
            url_txt.append({'url': url, 'text': soup.text})
        
    
    return url_txt
    
if __name__ == "__main__":
    t0 = time.time()
    
    actn = sys.argv[1]
    
    # total_nws_url_lst = gt_nws_urls()
    
    
    if actn == 'ggl_srch':
        #google search (first page)
        #TODO: add param for # pages of google results to look thru
        srch_on = input('What do you wanna google?  ')
        tot_ggl_urls = gt_ggl_urls(srch_on)
        
        txt_lst_dct = gt_txt(tot_ggl_urls)
        
        print(f'Number of URLs Scraped: {len(txt_lst_dct)}')
        # print(txt_lst_dct)
        print(txt_lst_dct[3:7])
        
        tknz_cls = Tokenize('')
        stpwrds = tknz_cls.gt_stpwrds()
        
        for data_dct in txt_lst_dct[:10]:
            print(data_dct)
            tknz_cls = Tokenize(data_dct['text'])
            #first sweep, remove \n in text
            tknz_cls.rmv_pnc(pnc_lst=['\n'], rplc=' ')
            print(tknz_cls.txt)
            #second sweep, look for all punctuation
            tknz_cls.rmv_pnc()
            print(tknz_cls.txt)
            #split up string by spaces
            tknz_cls.tknz()
            #remove white space
            tknz_cls.rmv_whtsp()
            #now remove typical English stopwords
            tknz_cls.rmv_stpwrds(stpwrds)
            #put list of strings back together
            # tknz_cls.cnctnt()
            # print(tknz_cls.txt)
            tknz_cls.lwr()
            tknz_cls.cnctnt()
            #remove numbers
            tknz_cls.rmv_stpwrds(['0','1','2','3','4','5','6','7','8','9'])
            x1 = tknz_cls.wrd_cnt()
            
            
            
    
    print(f'Script took {time.time()-t0}s to run.')
    
