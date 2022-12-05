#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:11:23 2022

Script holds classes peratining to text analysis.

@author: carl
"""

from collections import Counter
import math
import string

class Tokenize():
    '''Class to take in text and tokenize.'''
    
    def __init__(self, inpt_txt):
        self.txt = inpt_txt
        
    def cnctnt(self, delim=None):
        '''func to rejoin text if split up in list'''
        
        if delim is None:
            self.txt = ' '.join(self.txt)
        else:
            self.txt = delim.join(self.txt)
            
        return None
    
    
    def gt_stpwrds(self):
        '''func to read in stopwords from text file in repo
           taken from https://countwordsfree.com/stopwords'''
        
        stp_wrds = []
        with open('stop_words_english.txt') as g:
            stp_wrds = g.readlines()

        stp_wrds = [wrd.replace('\n', '') for wrd in stp_wrds]
            
        return stp_wrds
    
    
    def lwr(self):
        '''fnc to lowercase text'''
        if isinstance(self.txt, str):
            self.txt = self.txt.casefold()
        
        elif isinstance(self.txt, list):
            self.txt = [tkn.casefold() for tkn in self.txt]
            
        return None
        
        
    def rmv_pnc(self, pnc_lst=None, rplc=''):
        '''func to remove specified punctuation from inputted text'''
        
        if pnc_lst is None:
            pnc_lst = string.punctuation + '“”'
        
        if isinstance(self.txt, str):
            for pnc in pnc_lst:
                self.txt = self.txt.replace(pnc, rplc)
                
        elif isinstance(self.txt, list):
            tmp_txt = []
            for tkn in self.txt:
                for pnc in pnc_lst:
                   tkn = tkn.replace(pnc, rplc) 
                tmp_txt.append(tkn)
            self.txt =  tmp_txt
            
        return None
    

    def rmv_stpwrds(self, stpwrds=None, eq_tf=True):
        '''function to remove a list of stop words'''
        
        if stpwrds is None:
            stpwrds = self.gt_stpwrds()
        
        if isinstance(self.txt, str):
            for stpwrd in stpwrds:
                # print(stpwrd)
                self.txt = self.txt.replace(stpwrd, '')
        
        elif isinstance(self.txt, list):
            #might want to add option for == vs in 
            for stpwrd in stpwrds:
                for tkn in self.txt:
                    if tkn.casefold() == stpwrd.casefold():
                        self.txt.remove(tkn)
                
        return None
        
    def rmv_whtsp(self):
        '''function to remove trailing/leading whitespace'''
        
        if isinstance(self.txt, str):
            self.txt = self.txt.strip()
        
        elif isinstance(self.txt, list):
            self.txt = [tkn.strip() for tkn in self.txt]
            
        return None
        
            
    def tknz(self, delim=None):
        '''func to split up inputted text by specified character 
           -- default is a space'''
        
        if delim is None or delim == ' ':  
            self.txt = self.txt.split()
        else:
            self.txt = self.txt.split(delim)
        
        return None

    def wrd_cnt(self):
        '''func to count words or phrases'''
        
        if isinstance(self.txt, str):
            self.tknz()
            return self.wrd_cnt()
        elif isinstance(self.txt, list):
            return dict(Counter(self.txt))
    
    def phrs(self, phrs_lngth):
        '''func to chunk text into phrases given a phrase length'''
        
        if isinstance(self.txt, str):
            self.tknz()
            self.phrs(phrs_lngth)
        elif isinstance(self.txt, list):
            phrs_lst_lst = [self.txt[indx : indx+phrs_lngth] for indx, i in enumerate(self.txt)]
            self.txt = [' '.join(phrs_lst) for phrs_lst in phrs_lst_lst]
        
    
class TFIDF(Tokenize):
    
    def __init__(self, vrbs_tf=False):
        super().__init__('')
        self.vrbs_tf = vrbs_tf
        
    def trm_frq(self, tkn, txt):
        '''func to count number of times token appears'''
        
        self.txt = txt
        self.lwr()
        self.phrs(len(tkn.split(' ')))
        wrd_cnt_dct = self.wrd_cnt()
        
        tot_nm_tkn = sum(wrd_cnt_dct.values())
        
        tkn = tkn.casefold()
        if tkn in [ky.casefold() for ky in wrd_cnt_dct.keys()]:
            if self.vrbs_tf:
                print(f'{tkn} showed up {wrd_cnt_dct[tkn]} time(s)')
            self.tf = wrd_cnt_dct[tkn]/tot_nm_tkn
        else:
            if self.vrbs_tf:
                print(f'{tkn} did not show up')
                # print(list(wrd_cnt_dct.keys()))
            self.tf =  0
        

    def inv_doc_frq(self):
        '''func calculates inverse document frequency'''
        
        self.tot_nm_docs = len(self.tf_lst_dct)
        self.nm_docs_w_tkn = len([txt for txt in self.tf_lst_dct if txt['term_freq'] > 0])
        
        if self.nm_docs_w_tkn == 0:
            if self.vrbs_tf:
                print('Token did not appear in any documents.')
            self.df = 0
        else:
            self.df = math.log10(self.tot_nm_docs/self.nm_docs_w_tkn)
    
    
    def calc_tfidf(self, tkn, txt_lst_dct, preprcss_tf=False):
        '''func calculates tfidf given a list of dictionaries of text 
           (each element being a document) and a term'''
        
        self.tf_lst_dct = txt_lst_dct
        for txt in self.tf_lst_dct:
            if preprcss_tf:
                self.txt = txt['text']
                self.rmv_pnc()
                self.lwr()
                self.tknz()
                self.rmv_whtsp()
                txt['text'] = self.txt 
                
            self.trm_frq(tkn, txt['text'])
            txt['token'] = tkn
            txt['term_freq'] = self.tf
            
        self.inv_doc_frq()
        
        for doc in self.tf_lst_dct:
            # print(doc['term_freq'], self.df, self.tot_nm_docs, self.nm_docs_w_tkn)
            self.tfidf = doc['term_freq'] * self.df
            doc['tfidf'] = self.tfidf
            doc['doc_freq'] = self.nm_docs_w_tkn

        if self.vrbs_tf:
            print(self.tf_lst_dct)