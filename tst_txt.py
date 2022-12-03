#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 12:55:56 2022

Script tests text anlysis class functions.

@author: carl
"""
from txt_anlyss import Tokenize

if __name__ == "__main__":
    
    tst_str_cln = '''I must not fear. Fear is the mind-killer. 
    Fear is the little-death that brings total obliteration. 
    I will face my fear. I will permit it to pass over me and through me. 
    And when it has gone past I will turn the inner eye to see its path. 
    Where the fear has gone there will be nothing. Only I will remain.'''
    
    
    tst_str_mssy = '''    I must% not fear. Fear is the mind-killer.     
    Fear is the little-death that brings total oblite**ration. 
    I will face my\\ Fear. I will permit! it to pass over me and through me. 
    And///when it has (gone ) past I will turn the INNER eye to see its path. 
    Where the fear has gone there-will_be nothing    . Only I will remain.'''
    
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
    
    