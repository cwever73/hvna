#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:11:23 2022

Script holds classes peratining to text analysis.

@author: carl
"""

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

