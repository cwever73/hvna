#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:55:56 2022

Script tests text anlysis class functions.

@author: carl
"""

import sys
import time
from txt_anlyss import Tokenize, TFIDF

def tst_tfidf():
    '''func tests TFIDF Calculator'''

    doc0 = 'Moses supposes his toeses are roses. But Moses supposes erroneously'
    doc1 = 'And Moses, he knowses his toeses aren\'t roses. As Moses supposes his toeses to be'
    
    tfidf_cls = TFIDF(vrbs_tf=True)
    
    print('Test with word not in docs:\n')
    tfidf_cls.calc_tfidf('quarter', [{'text': doc0}, {'text': doc1}])
   
    print('Test with no pre-processing:\n')
    tfidf_cls.calc_tfidf('Moses', [{'text': doc0}, {'text': doc1}])
    
    print('Test with word preprocessing:\n')
    tfidf_cls.calc_tfidf('Moses', [{'text': doc0}, {'text': doc1}], preprcss_tf=True)
    
    print('Test with word preprocessing:\n')
    tfidf_cls.calc_tfidf('toeses', [{'text': doc0}, {'text': doc1}], preprcss_tf=True)
    
    

def tst_tknzr():
    '''func tests Tokenize class'''
    
    tst_str_cln = '''I must not fear. Fear is the mind-killer. 
    Fear is the little-death that brings total obliteration. 
    I will face my fear. I will permit it to pass over me and through me. 
    And when it has gone past I will turn the inner eye to see its path. 
    Where the fear has gone there will be nothing. Only I will remain.'''
    
    
    tst_str_mssy = '''    I must% not fear. Fear is the mind-killer.     
    Fear is the little-death that brings total oblite**ration. 
    I will face my\\ Fear. I 3will permit! it to pass over me and  67 through me. 
    And///when it has (gone ) past I will turn the INNER eye to see its path. 
    Where the fear has gone there-will_be 09nothing    . Only I will remain.'''
    
    print(f'Original Messy String:\n{tst_str_mssy}')
    
    #initialize tokenize class
    tknz_cls = Tokenize(tst_str_mssy)
    
    #test removing punctuation
    tknz_cls.rmv_pnc()
    print(f'Removing All Punctuation:\n{tknz_cls.txt}')
    
    #test removing specified punctuation
    tknz_cls = Tokenize(tst_str_mssy)
    tknz_cls.rmv_pnc('%_')
    print(f'Removing Specific Punctuation % and _ :\n{tknz_cls.txt}')
    
    #test removing specified punctuation
    tknz_cls = Tokenize(tst_str_mssy)
    tknz_cls.rmv_pnc('%_', 'XX')
    print(f'Removing Specific Punctuation and replace with \'XX\':\n{tknz_cls.txt}')
    
    #test lowercasing
    tknz_cls = Tokenize(tst_str_mssy)
    tknz_cls.lwr()
    tknz_cls.rmv_pnc()
    print(f'Lowercasing All Text:\n{tknz_cls.txt}')
    
    #test tokenizing and stripping out white space
    tknz_cls.tknz()
    tknz_cls.rmv_whtsp()
    tknz_cls.cnctnt()
    print(f'Tokenizing, removing white space and rejoining tokens:\n{tknz_cls.txt}')
    
    tknz_cls.rmv_stpwrds(['fear', 'mind'])
    tknz_cls.tknz()
    tknz_cls.rmv_whtsp()
    tknz_cls.rmv_nmbrs()
    tknz_cls.cnctnt()
    print(f'Removing \'mind\' and \'fear\' and numerics from text:\n{tknz_cls.txt}')
   

if __name__ == "__main__":
    t0 = time.time()
    
    actn = sys.argv[1]
    
    if actn == 'tst_tknzr':
        tst_tknzr() 
    elif actn == 'tst_tfidf':
        tst_tfidf()
    
    
    print(f'Script took {time.time()-t0}s to run.')