# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 21:53:20 2023

@author: lgxsv2
"""
import pandas as pd
import os 
import glob


def plotOne(driver):
    dirs = os.path.join(driver, r'\GeomorphologyPaper\DataFolder\Products\dimensions_drySeason')
    x = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    y = []
    for year in x:
        fp = os.path.join(dirs, ('DS_13_'+str(year)+'.csv'))
        df = pd.read_csv(fp)
        df = df.dropna()
        y.append(len(df))
        
        
    return x, y

def plotTwo(driver):
    dirs = os.path.join(driver, r'\GeomorphologyPaper\DataFolder\Products\dimensions_fullYear')
    x = [2021, 2022, 2023]
    yDry = []
    yRest = []
    for year in x:
        fps = glob.glob(os.path.join(dirs, ('*'+str(year)+'.csv')))
        tempDry = []
        tempRest = []
        for ds in fps:
            df = pd.read_csv(ds)
            df = df.dropna()
            dfDry = len(df[df['date'].astype(str).str.slice(4,6).isin(['07', '08', '09', '10'])])
            dfRest = len(df)-dfDry
            tempDry.append(dfDry)
            tempRest.append(dfRest)
        # manually adding extra
        if year == 2023:
            yDry.append(sum(tempDry))
            #  DS01==17,DS13==3, DS14==8, DS24==16, DS34==19 :: 63
            yRest.append(sum(tempRest)+63)
        else:
            yDry.append(sum(tempDry))
            yRest.append(sum(tempRest))
        
    
    return x, yDry, yRest

def plotThree(driver):
    # something to do with gettinf the ds valuesz
    dirs = os.path.join(driver, r'\GeomorphologyPaper\DataFolder\Products\dimensions_drySeason\*2023.csv')
    x = []
    fps = sorted(glob.glob(dirs))
    for i in fps:
        df = pd.read_csv(i)
        df = df.dropna()
        x.append(len(df))
    z = list(range(len(fps)))
    
    # y
    y = os.path.join(driver, "\GeomorphologyPaper\DataFolder\Products\dictionaries\channelSizes.csv")
    y = pd.read_csv(y)
    y = list(y['imsize'])
    # x = polygon size
    # y = number of images
    # z = distnace ds
    return x, y, z    

df = plotThree('D:')