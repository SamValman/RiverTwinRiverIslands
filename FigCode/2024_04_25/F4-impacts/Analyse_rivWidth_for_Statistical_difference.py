# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 22:20:25 2024

@author: lgxsv2
"""
import skimage.io as IO
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt
import numpy as np
from scipy.ndimage import convolve
import cv2 
import os
import glob
os.chdir(r"D:\GeomorphologyPaper\Analysis\Figures\funcs")
from F_impacts import calculateCenterline


# im = r"D:\GeomorphologyPaper\DataFolder\Imagery\m20Masks\2023\DS_13_20230607.tif"
# im = IO.imread(im)





#%%

def samSimpleWidth(dist, cl):
    clDist = dist * cl
    clDist *= 2
    return clDist


def widthVars(fn):
    im = IO.imread(fn)
    cl, dist = calculateCenterline(im)

    # widthIm
    w = samSimpleWidth(dist, cl)
    maxi = w.max()
    try:
        mini = min([num for row in w for num in row if num != 0])
    except:
        print('hmm')
        mini = -999

    return maxi, mini

def csvWidths(year=2023, ds='DS_13', driver='D:'):
    folderPath = os.path.join(os.path.join(os.path.join(driver, r'\GeomorphologyPaper\DataFolder\Imagery\m20Masks'), str(year)), (ds +'*.tif'))
    maxis, minis, dates = [],[], []
    for i in glob.glob(folderPath):
        maxi, mini = widthVars(i)
        maxis.append(maxi)
        minis.append(mini)
        date = i[-12:-4]
        dates.append(date)
    df = pd.DataFrame({'date':dates, 'max':maxis,'min':minis})
    op = os.path.join(os.path.join(driver + '\GeomorphologyPaper\DataFolder\Products\centerlinewidths'), (str(year)+ds+".csv"))
    df.to_csv(op, index=False)
    print(ds,': DONE' )
# im = CalculateOrthAngle(im)
# width = CalculateWidth(im)

def getCSVs(year=2023, driver='D:'):
    for i in range(0, 35):
        if i <=9:
            ds = 'DS_0'+str(i)
        else:
            ds = 'DS_'+str(i)
        csvWidths(year, ds, driver)
        

#%%
getCSVs()


#%%
# # create function that scrolls through 
# # prints max and min to csv,
# # csv for each ds

def stats(driver='D:'):
    fp = os.path.join(os.path.join(driver, r'\GeomorphologyPaper\DataFolder\Products\centerlinewidths'),'2023*.csv')
    octs, junes, maxi, mini, change, ds = [],[],[],[],[],[]
    for i in glob.glob(fp):
        df = pd.read_csv(i)
        ds.append(i[-9:-4]) # check
        # do something to make just june to october
        df = df[df['date']>20230540]
        df = df[df['date']<202301100]
        maxi.append(df['max'].max())
        mini.append(df['max'].min())
        junes.append(df.iloc[1,:]['max'])
        octs.append(df.iloc[-1, :]['max'])
        change.append((df.iloc[1,:]['max'])-(df.iloc[-1,:]['max']))
    # get path
    
    df = pd.DataFrame({'ds':ds, 'change':change, 'maxJune':junes, 'maxOct':octs, 'max':maxi, 'min':mini})
    df.to_csv(os.path.join(driver, r'D:\GeomorphologyPaper\DataFolder\Products\centerlinewidths\total.csv'), index=False)
    return df
# then another function that reads csvs, takes first and last, max and min into a single csv for everywhere
#%%

# df = stats()

from scipy.stats import ttest_rel, shapiro


def pairedTest(driver='D:'):
    df = pd.read_csv(os.path.join(driver, r'D:\GeomorphologyPaper\DataFolder\Products\centerlinewidths\total.csv'))
    t_statistic, p_value = ttest_rel(df['maxJune'], df['maxOct'])
    
    
    # Shapiro-Wilk test for normality
    statistic, p_value = shapiro(df['change'])
    
    print("Shapiro-Wilk Test:")
    print(f'Statistic: {statistic}')
    print(f'P-value: {p_value}')
    print(' ')

    # Print the results
    print("Paired Two-Sample T-Test:")
    print(f'T-statistic: {t_statistic}')
    print(f'P-value: {p_value}')
    print(' ')

    print('average change: ', df['change'].mean())   
    print('max change: ', df['change'].max())
    print('min change: ', df['change'].min())
    print('range: ', df['change'].max()-df['change'].min())


    return df
    
df = pairedTest()



