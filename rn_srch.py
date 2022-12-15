#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 20:09:31 2022

@author: carl
"""

import subprocess
import time


if __name__ == '__main__':
    
    
    try:
        rn_scrpt = int(input('How many days do you want to run this?\t'))
    except:
        rn_scrpt = int(input('''The value you entered was not an integer.
                             Please type in the number of days you wish to 
                             run this script:\t'''))
    
    while rn_scrpt != 0:
        subprocess.run(['python gt_txt.py gt_nws'], shell=True)
        #wait 24hrs
        time.sleep(86400)
        rn_scrpt -= 1
    
    