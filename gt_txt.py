#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 14:06:11 2022

Script gets text from desired urls.

@author: carl
"""

from bs4 import BeautifulSoup as btflSp
from datetime import datetime as dt
import os
import requests
import sys
import time
from txt_anlyss import Tokenize, TFIDF
import yaml


def gt_ggl_urls(srch_trm):
    '''func to grab urls from a particular google search'''
    
    skp_dmns = ('https://www.google.', 
                'https://google.', 
                'https://webcache.googleusercontent.', 
                'http://webcache.googleusercontent.', 
                'https://policies.google.',
                'https://support.google.',
                'https://maps.google.',
                 'https://www.youtube.com')
    
    srch_trm = srch_trm.replace(' ', '+')
    url = f'https://www.google.com/search?q={srch_trm}'
    print(f'URL: {url}')
    reqs = requests.get(url)
    print('###########################')
    
    soup = btflSp(reqs.text, 'html.parser')
    
    ggl_url_lst = []
    for indx, link in enumerate(soup.find_all('a')):
        print(indx, link.get('href'))
        
        skip_tf = False
       
        for ggl_dmn in skp_dmns:
            if ggl_dmn == link.get('href')[len('/url?q='):len('/url?q=')+len(ggl_dmn)]:
                skip_tf = True #just a site we dont care about (standard google sites, youtube)
        
        if not skip_tf:
            if '/url?q=' in link.get('href'):
                    nw_url = link.get('href').split('/url?q=')[1].split('&sa=U&ved')[0]
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


def tfidf_ggl_srch(srch_on, flnm):
    '''given a term to search for and a filename, wrtie tfidf scores
       for all urls on first page of google result for tokens up to length 3'''

    #TODO: add param for # pages of google results to look thru
    #TODO: maybe make phrase length a variable

    tot_ggl_urls = gt_ggl_urls(srch_on)
    
    txt_lst_dct = gt_txt(tot_ggl_urls)
    
    print(f'Number of URLs Scraped: {len(txt_lst_dct)}')
    
    tot_srch_lst = []
    for data_dct in txt_lst_dct:
        # print(data_dct)
        # print(data_dct['text'][-500:])
        tknz_cls = Tokenize(data_dct['text'])
        #first sweep, remove \n in text
        tknz_cls.rmv_pnc(pnc_lst=['\n', '\t', '\r'], rplc=' ')
        #second sweep, look for all punctuation
        tknz_cls.rmv_pnc(rplc=' ')
        #split up string by spaces
        tknz_cls.tknz()
        #remove white space
        tknz_cls.rmv_whtsp()
        #now remove typical English stopwords
        tknz_cls.rmv_stpwrds()
        #put list of strings back together
        tknz_cls.lwr()
        #remove numbers
        tknz_cls.rmv_nmbrs()
        #remove those blanks in list of text
        tknz_cls.rmv_gnrl('')
        # print(tknz_cls.txt)
        data_dct['word_count'] = tknz_cls.wrd_cnt()
        data_dct['text'] = tknz_cls.txt
        
        #get list of tokens to calculate tfidf
        mx_phrs_lngth = 3 #search for phrases up to 3 words in length
        for phrs_lngth in range(1, mx_phrs_lngth+1):
            phrs_lst_lst = [tknz_cls.txt[indx : indx+phrs_lngth] for indx, i in enumerate(tknz_cls.txt)]
            phrs_lst = [' '.join(phrs_lst) for phrs_lst in phrs_lst_lst]
            tot_srch_lst += phrs_lst
        
    tot_srch_lst = list(set(tot_srch_lst))
    #create dictionary of all token's tfidf scores
    tfidf_dct = {}
    tfidf_cls = TFIDF() 
    print('**************************')
    print(f'Total Number of Tokens to Search for: {len(tot_srch_lst)}')
    for indx, tkn in enumerate(tot_srch_lst):
        if indx > 0:
            if indx%2701 == 0:
                print(indx/len(tot_srch_lst))
                
        tfidf_cls.calc_tfidf(tkn, txt_lst_dct)
        if tfidf_cls.tfidf > 0:
            tfidf_dct[tkn] = {'tfidf': tfidf_cls.tfidf, 'df': tfidf_cls.nm_docs_w_tkn}
        
    print(tfidf_dct)
    print(f'Saving results here: {flnm}')
    with open(flnm, 'w+') as f:
        yaml.dump(tfidf_dct, f, allow_unicode=True)
    
    
    
if __name__ == "__main__":
    t0 = time.time()
    
    actn = sys.argv[1]
    
    
    if actn == 'gt_nws':
        
        # flnm = input('Enter yaml that holds tfidf scores:  ')
        
        # with open(flnm) as f:
            # tfidf_dct_new = yaml.load(f, yaml.SafeLoader)
        
        tot_nws_url_lst = gt_nws_urls()
        
        txt_lst_dct = gt_txt(tot_nws_url_lst)
        
        print(f'Number of URLs Scraped: {len(txt_lst_dct)}')
        
        bzz_wrds = ['neuroscience', 'cuba', 'ring', 'ringing', 'illness', 
                  'mysterious', 'loud noise', 'ear', 'ears', 'pressure',
                  'vibrations', 'head', 'concussion', 'tinnitus', 'vertigo',
                  'nausea', 'cognitive difficulties', 'cognitive', 'embassy'
                  'embassies', 'agent', 'agents', 'ambassador', 'ambassadors',
                  'sonic', 'attack', 'diplomat', 'diplomats', 'noise', 'noises'
                  'grating noises', 'grating', 'strange', 'home', 'hotel', 
                  'hotels', 'hotel room',  'hotel rooms', 'device', 'beam',
                  'memory loss', 'hearing loss', 'nausea'
                  ]
        
        for data_dct in txt_lst_dct:
            cnt = 0
            tknz_cls = Tokenize(data_dct['text'])
            #first sweep, remove \n in text
            tknz_cls.rmv_pnc(pnc_lst=['\n'], rplc=' ')
            #second sweep, look for all punctuation
            tknz_cls.rmv_pnc(rplc=' ')
            #split up string by spaces
            tknz_cls.tknz()
            #remove white space
            tknz_cls.rmv_whtsp()
            #now remove typical English stopwords
            tknz_cls.rmv_stpwrds()
            #put list of strings back together
            tknz_cls.lwr()
            #remove numbers
            tknz_cls.rmv_nmbrs()
            #put it back
            tknz_cls.cnctnt()
            for bzz in bzz_wrds:
                if bzz in tknz_cls.txt:
                    cnt += 1
            data_dct['bzz_tkn_num'] = cnt
            
            print(data_dct['url'], data_dct['bzz_tkn_num'])
            
        
    
    if actn == 'tfidf_ggl_srch':
        
        srch_trm = input('What do you wanna google?  ')
        
        pth = input('Enter path to store tfidf scores:  ')
        
        flnm = os.path.join(pth, f"tfidf_scores_{srch_trm.replace(' ', '_')}_search.yaml")
        
        tfidf_ggl_srch(srch_trm, flnm)
        
            
    print(f'Script took {time.time()-t0}s to run.')