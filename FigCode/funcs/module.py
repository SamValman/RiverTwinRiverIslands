# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:44:55 2023

@author: lgxsv2
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:11:05 2023

@author: lgxsv2
"""
import rasterio as rio
import glob 
import os
import skimage.io as IO
import numpy as np
import pandas as pd
import pathlib


#%%
# function list - all need to be camel case.
#  1. tifProjection
#  2. getStackHeight
#  3. convertBase0
#  4. organiseDate



#%%




def tifProjection(fn_in, fn_raw='x', out='x'):
    '''
    Adds geolocation data to imagery 
    **REQUIRES: temporary saving of image to be located.
    
    Parameters
    ----------
    fn_in : Str fn
        water mask p3 from River Twin Water Mask.Or other un located image
    fn_raw : Str fn
        raw tiff image used for the water mask.
    out : Str fn
        fn to save new located image. 

    Returns
    -------
    saves located image.

    '''
    
    
    with rio.open(fn_in) as m:
        im = m.read()
        profile_old = m.profile
    
    print('old profile:')
    print(profile_old)
    
    with rio.open(fn_raw) as i:
        profile = i.profile
        profile['count']=1
    print('new profile:')
    print(profile)
    
    # return profile

    # save file with new/old profile
    with rio.open(out, 'w', **profile) as l:
        l.write(im)
    print('complete')

#%%
def getStackHeight(fp,ds):
    '''
    Parameters
    ----------
    fp : path
        the Downstream polygon number and a *.tif are added.
    ds : str e.g., "DS_01"
        the Downstream number you want stacked.

    Returns
    -------
    im : array
        stacked image of land occurance in the images.

    '''
    fp = os.path.join(fp,(ds+'*.tif') )
    ls = []
    for i in glob.glob(fp):
        ti = IO.imread(i)
        if ds=='DS_34':
            if ti.shape!= (2519, 3079):
                continue
        ti = 1 - ti
        ls.append(ti)
    im = np.sum(ls, axis=0)
    im = im.astype(int)
    return im 

#%%
def convertBase0(df, ds, dirs=''):
    '''
    May need to change this because it currently changes depending on if there is a high water date
    ONLY AN ISSUE WITH FULL YEAR RESULTS

    Parameters
    ----------
    df : pd.df
        ds_Df.
    ds : str
        "DS_00"to "DS_34".
    dictionary : path
        DESCRIPTION. for the harddrive r"\GeomorphologyPaper\DataFolder\Products\dictionaries\channelSizes.csv".
for the harddrive
    Returns
    -------
    df : pd.df
        df with new base value from 1st image in the df.

    '''
    # get the pre established dictionary of image bank sizes
    drive = pathlib.Path(dirs).drive

    dictionary = os.path.join(drive, r"\GeomorphologyPaper\DataFolder\Products\dictionaries\channelSizes.csv")
    dictionary = pd.read_csv(dictionary)
    
    # get the imsize for the ds in question 
    num = dictionary[dictionary['id']==ds]['imsize']
    
    # check for errors in area value or date in the ds df
    df.dropna(subset=['date'], inplace=True)
    df = df[pd.to_numeric(df['area'], errors='coerce').notnull()]
    
    # y is the working var
    y = df.area
    if y.dtype== object:
        y = y.astype(int)

    # get percentage of actual channel that is land
    y = (y/int(num.iloc[0]))*100
    
    # set base to 0
    y = y - y.iloc[0]
    
    # add to df and return
    df['base']=y
    
    return df


#%% Not sure if needed ###*****#'#' not finished yet
def organiseDate(df, form = '%m%d', monthday=True):
    if monthday:
        df['date'] = df['date'].astype(str).str[-4:]  # get monthday
    df['date'] = pd.to_datetime(df['date'], format=form, errors='coerce')
    # df['month_day'] = df['date'].dt.strftime('%m%d')
    df = df.sort_values(by="date")

    return df


#%%

def smoothLines(df, var='base', roll=3):
    '''
    Smooths lines with rolling average 

    Parameters
    ----------
    df : pd.df or pd.series
        df of date and either slope or change or whatever.
    var : str, optional
        Var in df being smoothed. The default is 'base'.
    roll : int, optional
        number of vals to smooth. The default is 3.

    Returns
    -------
    df : original but smoothed
        DESCRIPTION.

    '''
    # check if df or series (derivitives)
    if isinstance(df, pd.DataFrame):
        # smooth the df with a rolling avg
        df[var] = df[var].rolling(roll).sum()
    else:
        df = df.rolling(roll).sum()
    
    return df
    









