# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 01:40:17 2024

@author: lgxsv2
"""

import os
import pandas as pd 
os.chdir(r"D:\GeomorphologyPaper\Analysis\Figures\funcs")
import module

def F3Stats(ls_ds, dirs=r"D:\GeomorphologyPaper\DataFolder\Products\dimensions_drySeason"):
    '''
    provides: max, min, date over 50%
    '''
    maxes = []
    dates = []
    for cnumber, ds in enumerate(ls_ds):
        
        
        # get the csv for 2023 dry season
        csv = os.path.join(dirs, (ds+'_2023.csv'))
        df = pd.read_csv(csv)
        
        # convert 
        df = module.convertBase0(df, ds)
        maxes.append(df['base'].max())

        # get 50%
        dif = ((df['base'].max()-df['base'].min())/2)+df['base'].min()
        df = df[df['base']<=dif]
        d = df.iloc[-1,:]['date']
        dates.append(d)
        print(str(ds)+': '+str(d))
        
        
        
        
    df = pd.DataFrame({'ds':ls_ds, 'max':maxes})
    
    print('max: ')
    toPrint = df[df['max']==max(maxes)].copy()
    print(toPrint)
    
    print('min: ')
    toPrint = df[df['max']==min(maxes)].copy()
    print(toPrint)
    print(' ')

    
    print('50% date: ')
    toPrint=max(dates)
    print(toPrint)
    print(' ')
    print(' ')
    print(' ')

    
    
    
        
ds = [ 'DS_01', 'DS_02','DS_04', 'DS_05','DS_06','DS_07','DS_08', 'DS_09', 'DS_10',
    'DS_11', 'DS_12', 'DS_13','DS_14', 'DS_15','DS_16','DS_17','DS_18',
    'DS_19','DS_20', 'DS_24', 'DS_25', 'DS_26', 'DS_27', 'DS_28', 'DS_29', 
    'DS_30', 'DS_31', 'DS_32', 'DS_33', 'DS_34']

F3Stats(ls_ds=ds)


