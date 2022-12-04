#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:11:23 2022

Script holds classes peratining to text analysis.

@author: carl
"""

from collections import Counter
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
            pnc_lst = string.punctuation
        
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
                print(stpwrd)
                self.txt = self.txt.replace(stpwrd, '')
        
        elif isinstance(self.txt, list):
            #might want to add option for == vs in 
            for stpwrd in stpwrds:
                for tkn in self.txt:
                    if tkn == stpwrd:
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
        
        
    
class TFIDF(Tokenize):
    
    def __init__(self, txt_dct):
        self.txt_dct = txt_dct
        super().__init__('')
        
    def tf(self, tkn, txt):
        '''func to count number of times token appears in already tokenized text'''
        lngth =len(tkn.split(' '))
        phrs_lst_lst = [txt[indx : indx+lngth] for indx, i in enumerate(txt)]
        self.txt = [' '.join(phrs_lst) for phrs_lst in phrs_lst_lst]
        wrd_cnt_dct = self.wrd_cnt()
        
        
        

    def df(self):
        pass

