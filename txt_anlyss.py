#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:11:23 2022

@author: carl
"""

import string

class Tokenize():
    '''Class to take in text and tokenize.'''
    
    def __init__(self, inpt_txt):
        self.txt = inpt_txt
        
    def rmv_pnc(self, pnc_lst=None):
        '''func to remove specified punctuation from inputted text'''
        
        if pnc_lst is None:
            pnc_lst = string.punctuation
        
        if isinstance(self.txt, str):
            for pnc in pnc_lst:
                self.txt = self.txt.replace(pnc, '')
                
        elif isinstance(self.txt, list):
            tmp_txt = []
            for tkn in self.txt:
                for pnc in pnc_lst:
                   tkn = tkn.replace(pnc, '') 
                tmp_txt.append(tkn)
            self.txt =  tmp_txt
            
    def rmv_whtsp(self):
        '''function to remove trailing/leading whitespace'''
        
        if isinstance(self.txt, str):
            self.txt = self.txt.strip()
        
        elif isinstance(self.txt, list):
            self.txt = [tkn.strip() for tkn in self.txt]
        
            
    def tknz(self, delim=' '):
        '''func to split up inputted text by specified character 
           -- default is a space'''
           
        self.txt = self.txt.split(delim)

